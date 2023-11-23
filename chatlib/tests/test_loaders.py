"""Test chatlib.wikijs.loaders."""

import os

import pytest

from chatlib.wikijs.loaders import get_session, list_all_pages, search_by_keywords
from chatlib.wikijs.models import Page, PageListItem


@pytest.fixture
def wikijs_api_token():
    """Get API token for WikiJS's API."""
    return os.environ["WIKIJS_API_TOKEN"]


@pytest.mark.asyncio
@pytest.fixture
async def session_coro(wikijs_api_token):
    """Get session as soroutine."""
    return get_session("https://wiki.knml.edu.pl", wikijs_api_token)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_list_pages(session_coro):
    """Test listing ALL pages on WikiJS."""
    min_pages = 5
    session = await session_coro  # Needs to bo awaited
    async with session:
        pages = await list_all_pages(session, "pl")
    assert (
        len(pages) > min_pages
    ), f"There should be at least {min_pages} pages in the wiki. Check if your token is valid."
    assert all(
        isinstance(page, PageListItem) for page in pages
    ), "All pages should be of type Page"


@pytest.mark.asyncio
@pytest.mark.integration
async def test_search_by_keywords(session_coro):
    """Test searching by keyword on WikiJS."""
    session = await session_coro  # Needs to bo awaited
    async with session:
        pages = await search_by_keywords(session, ["KNML"], "pl")
    assert (
        len(pages) > 0
    ), "There should be at least 1 page with KNML keyword. Check if your token is valid."
    assert all(
        isinstance(page, Page) for page in pages
    ), "All pages should be of type Page"
