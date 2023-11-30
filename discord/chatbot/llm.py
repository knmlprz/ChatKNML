import os
import aiohttp
import json
import logging

logger = logging.getLogger(__name__)

COMPLETIONS_API_URL = os.environ.get(
    "COMPLETIONS_API_URL", "http://llamacpp:8080/completion"
)

COMPLETION_PROMPT_FILE = os.environ.get(
    "COMPLETION_PROMPT_FILE", "sheep-duck-llama2-70B.txt"
)

with open(os.path.join("prompts", COMPLETION_PROMPT_FILE), "r") as f:
    COMPLETION_PROMPT = f.read()
    logging.debug("Loded prompt: %s", COMPLETION_PROMPT)


async def query_llm(
    query: str,
    prompt: str = COMPLETION_PROMPT,
    completions_api: str = COMPLETIONS_API_URL,
    max_tokens: int = 3000,
    temperature: float = 0.7,
) -> str:
    """Query and LLM on OpenAI-like /completions API Endpoint.

    This function comes with pre-formatted prompt that is tied to the model used.

    Args:
        query: Query from user.
        prompt: Chat prompt template for LLM.
        completions_api: OpenAI like completions api endpoint.
        max_tokens: The maximum number of tokens to generate in the chat completion.
        temparature: What sampling temperature to use, between 0 and 2.
            Higher values like 0.8 will make the output more random, while
            lower values like 0.2 will make it more focused and deterministic.
    """
    logger.info("query_lmm: %s", query)
    formatted_prompt = prompt.format(query)
    logger.debug("query_llm: %s", formatted_prompt)
    headers = {"content-type": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.post(
            completions_api,
            json={
                "prompt": formatted_prompt,
                "n_predict": max_tokens,
                "temperature": temperature,
            },
            headers=headers,
        ) as response:
            text = await response.text()
            logger.info("Got response: %s", text)
            data = json.loads(text)
    return data["content"]
