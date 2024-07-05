from http import HTTPStatus

import requests
from langchain_openai import OpenAI
from pgvector.django import L2Distance

from bot.schemas import BotIn, BotOut
from chunks.models import Chunk


def query_llm_controller(payload: BotIn) -> tuple[HTTPStatus, BotOut]:
    embeddings_body = {
        "input": payload.input
    }
    response = requests.post("http://192.168.0.3:9000/v1/embeddings/", json=embeddings_body)
    input_embedding = response.json()['data'][0]['embedding']
    similar_chunk = Chunk.objects.order_by(L2Distance('embedding', input_embedding))[0]
    model_url = "http://192.168.0.3:9000/v1/"
    llm = OpenAI(temperature=0.5,
                 openai_api_key="XD",
                 openai_api_base=model_url
                 )
    llm_response = llm.invoke(
        "Odpowiedz na pytanie używając 5 zdań" + payload.input + "\n\nWiedząc że" + similar_chunk.text)
    return HTTPStatus.OK, BotOut(output=str(llm_response))
