from typing import Literal
from openai import AsyncOpenAI

smol_model_client = AsyncOpenAI(
    api_key="XD",
    base_url="http://host.docker.internal:8001",
)

big_model_client = AsyncOpenAI(
    api_key="XD",
    base_url="http://host.docker.internal:8000",
)

PROMPT = """
Jesteś AI działającym na discordzie Koła Naukowego Machine Learning Politechniki Rzeszowskiej.
W skrócie (KNML PRz). Jesteś tutaj, aby pomóc ludziom w ich problemach związanych z ML. 

1. Bądź miły i uprzejmy.
2. Każdą odpowiedź zakończ emotką.

Pytanie: {}
Odpowiedź: 
"""


async def ask_model(question: str, model: Literal["smol", "big"]):
    client = None
    match model:
        case "smol":
            client = smol_model_client
        case "big":
            client = big_model_client

    response = await client.completions.create(
        model="DOESNT MATTER",  # Literally doesn't matter
        prompt=PROMPT.format(question),
        max_tokens=200,
        temperature=0.7,
        n=1,  # Number of completions to generate
    )

    return response.choices[0].text
