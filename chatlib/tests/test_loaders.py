import pytest
import os

from chatlib.wikijs.loaders import get_session, list_pages, search_by_keywords
from chatlib.wikijs.models import PageListItem, Page

@pytest.fixture
def wikijs_api_token():
    api_token = os.getenv("WIKIJS_API_TOKEN")
    if api_token is None:
        raise ValueError("WIKIJS_API_TOKEN is not set")
    return api_token

@pytest.mark.asyncio
@pytest.fixture
async def session_coro(wikijs_api_token):
    session = get_session("https://wiki.knml.edu.pl", wikijs_api_token)
    return session

@pytest.mark.asyncio
@pytest.mark.integration
async def test_list_pages(session_coro):
    session = await session_coro # Needs to bo awaited 
    async with session:
        pages = await list_pages(session, "pl")
    assert len(pages) > 5, "There should be at least 5 pages in the wiki. Check if your token is valid."
    assert all(isinstance(page, PageListItem) for page in pages), "All pages should be of type Page"
    

@pytest.mark.asyncio
@pytest.mark.integration
async def test_search_by_keywords(session_coro):
    session = await session_coro # Needs to bo awaited
    async with session:
        pages = await search_by_keywords(session, ["KNML"], "pl")
    assert len(pages) > 0, "There should be at least 1 page with KNML keyword. Check if your token is valid."
    assert all(isinstance(page, Page) for page in pages), "All pages should be of type Page"
