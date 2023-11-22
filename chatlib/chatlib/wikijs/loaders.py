import aiohttp
import asyncio
import logging

from typing import List

from .models import Page, PageListItem

logger = logging.getLogger(__name__)


def get_session(url: str, token: str):
    """
    Generate aiohttp session with authentication headers

    Args:
        url: GraphQL endpoint url
        token: Authentication token
    """

    # Build headers
    headers = {"Authorization": f"Bearer {token}"}

    # Create session
    session = aiohttp.ClientSession(base_url=url, headers=headers)
    logger.debug(f"Created session with base url {url}")
    return session


async def _get_page_id(session: aiohttp.ClientSession, path: str, locale: str) -> int:
    query = """
    query ($path: String!, $locale: String!) {
        pages {
            tree(path: $path, locale: $locale, mode: ALL) {
                id
                path
                title
            }
        }
    }
    """
    resp = await session.post(
        "/graphql", json={"query": query, "variables": {"path": path, "locale": locale}}
    )
    data = await resp.json()
    pages = [
        PageListItem(
            **page,
        )
        for page in data["data"]["pages"]["tree"]
    ]

    # Find exact match of path
    for page in pages:
        if page.path == path:
            return page.id
    raise ValueError("Page does not exist on a path.")


async def _fix_pageid(
    session: aiohttp.ClientSession, page: PageListItem, locale: str
) -> PageListItem:
    page.id = await _get_page_id(session, page.path, locale=locale)
    return page


async def _get_page(session: aiohttp.ClientSession, page_id: int, locale: str) -> Page:
    """Get page with content

    Args:
        session: aiohttp session
        page_id: Page ID

    Returns:
        Page or None if page does not exist or is not accessible (unauthorized)
    """
    query = """
    query ($id: Int!) {
        pages {
            single(id: $id) {
                id
                path
                title
                description
                content
            }
        }
    }
    """
    logger.debug("Getting page with id %s", page_id)
    resp = await session.post(
        "/graphql", json={"query": query, "variables": {"id": page_id}}
    )
    logger.debug(
        "Got response from wiki for Page with id %s. Response status: %s, Response text: %s",
        page_id,
        resp.status,
        await resp.text(),
    )

    data = await resp.json()
    # Check if response is not an error
    if "errors" in data:
        raise PermissionError(data["errors"][0]["message"], "page_id", page_id)

    page = Page(
        **data["data"]["pages"]["single"],
        instance_url=str(session._base_url),
        locale=locale,
    )
    return page


async def _list_by_keyword(
    session: aiohttp.ClientSession, keyword: str, locale: str
) -> List[PageListItem]:
    """List pages by keyword. Even pages that you don't have access to!

    Args:
        session: aiohttp session
        keyword: Keyword to search for

    Returns:
        List of page items (Pages without content)
    """
    query = """
    query ($keyword: String!) {
        pages {
            search(query: $keyword) {
                results {
                    id
                    path
                    title
                    description
                }
            }
        }
    }
    """
    resp = await session.post(
        "/graphql", json={"query": query, "variables": {"keyword": keyword}}
    )
    data = await resp.json()
    pages = [
        PageListItem(
            **page,
        )
        for page in data["data"]["pages"]["search"]["results"]
    ]
    # Fix page IDs
    # See: https://github.com/Requarks/wiki/issues/2938
    pages = await asyncio.gather(
        *[_fix_pageid(session, page, locale=locale) for page in pages]
    )
    return pages


async def search_by_keywords(
    session: aiohttp.ClientSession, keywords: List[str], locale: str
) -> List[Page]:
    """Search for pages by keywords

    Args:
        keywords: List of keywords
        locale: Locale of the wiki

    Returns:
        List of documents
    """
    results: List[List[PageListItem]] = await asyncio.gather(
        *[_list_by_keyword(session, keyword, locale=locale) for keyword in keywords]
    )
    logger.debug("Keyword search results: %s", results)
    
    page_items: List[PageListItem] = []
    for result in results:
        page_items.extend(result)
    # Filter out duplicates
    page_items = list(set(page_items))

    # Get pages, note that _list_by_keyword can return pages that
    # you don't have access to
    page_gather_results: List[Page | Exception] = await asyncio.gather(
        *[_get_page(session, page.id, locale) for page in page_items],
        return_exceptions=True,
    )

    # Filter out pages that you don't have access to
    def permission_error_filter(item: Page | Exception) -> bool:
        if not isinstance(item, Exception):
            return True
        logger.warning(item)
        return False

    return list(filter(permission_error_filter, page_gather_results))  # type: ignore


async def list_pages(session: aiohttp.ClientSession, locale: str) -> List[PageListItem]:
    """
    List all pages in wiki

    Args:
        session: aiohttp session

    Returns:
        List of pages
    """

    query = """
    query {
        pages {
            list (orderBy: TITLE) {
                id
                path
                title
            }
        }
    }
    """
    logger.debug("Listing pages from wiki on url: %s", session._base_url)
    resp = await session.post("/graphql", json={"query": query})

    logger.debug(
        "Got response from wiki. Response status: %s, Response text: %s",
        resp.status,
        await resp.text(),
    )
    data = await resp.json()

    logger.debug("Json: %s", data)
    pages_ = data["data"]["pages"]["list"]
    pages = [PageListItem(**item) for item in pages_]

    # Fix page IDs
    # See: https://github.com/Requarks/wiki/issues/2938
    pages = await asyncio.gather(
        *[_fix_pageid(session, page, locale=locale) for page in pages]
    )

    return pages
