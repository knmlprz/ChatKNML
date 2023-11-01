import aiohttp
import asyncio
import logging

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


async def list_pages(session: aiohttp.ClientSession) -> list[PageListItem]:
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
    
    logger.debug("Got response from wiki. Response status: %s, Response text: %s", resp.status, await resp.text())
    data = await resp.json()
    
    logger.debug("Json: %s", data)
    pages_ = data["data"]["pages"]["list"]
    pages = [PageListItem(**item) for item in pages_]
    return pages


async def get_page(session: aiohttp.ClientSession, page_id: int) -> Page | None:
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
    logger.debug("Got response from wiki for Page with id %s. Response status: %s, Response text: %s",page_id, resp.status, await resp.text())
    
    data = await resp.json()
    if session._base_url is None:
        raise ValueError("Base url is None")
    try:
        page = Page(**data["data"]["pages"]["single"], instance_url=str(session._base_url), locale="pl")
    except TypeError:
        return None
    return page


def cli():
    import argparse
    from pprint import pprint
    from dotenv import load_dotenv
    import os

    load_dotenv()

    parser = argparse.ArgumentParser(description="WikiJS Downloader")
    parser.add_argument("url", metavar="URL", type=str)
    parser.add_argument("-o", "--output", metavar="OUTPUT", type=str, default="output")
    parser.add_argument("-d", "--debug", action="store_true")

    if parser.parse_args().debug:
        # create console handler and set level to debug
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)
    args = parser.parse_args()

    url = args.url
    token = os.getenv("WIKIJS_TOKEN")
    if token is None:
        raise ValueError("WIKIJS_TOKEN is not defined in environment variables")
    loop = asyncio.get_event_loop()

    print(f"Downloading pages from {url}...")
    session = get_session(url, token)
    page_items = loop.run_until_complete(list_pages(session))
    #print(f"Downloaded {len(page_items)} pages")
    # pprint(page_items)

    pages_to_download = [get_page(session, page.id) for page in page_items]
    pages = loop.run_until_complete(asyncio.gather(*pages_to_download))
    #pprint(pages)
 
    loop.run_until_complete(session.close())
    #pprint(pages)
