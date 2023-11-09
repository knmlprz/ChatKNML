from typing import Literal
from openai import AsyncOpenAI

smol_model_client = AsyncOpenAI(
    api_key="XD",
    base_url="http://host.docker.internal:8001/v1",
)

big_model_client = AsyncOpenAI(
    api_key="XD",
    base_url="http://host.docker.internal:8000/v1",
)

PROMPT = """
Jesteś AI działającym na discordzie Koła Naukowego Machine Learning Politechniki Rzeszowskiej.
W skrócie (KNML PRz). Jesteś tutaj, aby im pomagać. 

1. Bądź miły i uprzejmy.
2. Każdą odpowiedź zakończ emotką.
3. Odpowiadaj w języku polskim.
4. Przerwij pisanie po udzieleniu odpowiedzi. 

Człowiek: {}
AI:  
"""


async def ask_model(question: str, model: Literal["smol", "big"]):
    client = None
    match model:
        case "smol":
            client = smol_model_client
        case "big":
            client = big_model_client

    prompt = PROMPT.format(question)
    print(prompt)

    response = await client.completions.create(
        model="DOESNT MATTER",  # Literally doesn't matter
        prompt=prompt,
        max_tokens=500,
    )

    return response.choices[0].text
