"""Test llm.py module."""
import asyncio
import json

from aioresponses import aioresponses

from discord_bot import llm


def test_query_llm():
    """Test query_llm function."""
    loop = asyncio.get_event_loop()
    correct_response = "IT WORKS"
    body = json.dumps(
        {
            "content": correct_response,
        },
    )
    with aioresponses() as m:
        headers_json = {"content-type": "application/json"}
        m.post(llm.COMPLETIONS_API_URL, status=200, body=body, headers=headers_json)
        resp = loop.run_until_complete(llm.query_llm("test"))
        assert resp == correct_response

        # Test whether function works if content-type is incorrect
        # for example: llamacpp's server returns text/plain
        headers_text = {"content-type": "text/plain"}
        m.post(llm.COMPLETIONS_API_URL, status=200, body=body, headers=headers_text)
        resp = loop.run_until_complete(llm.query_llm("test"))
        assert resp == correct_response
