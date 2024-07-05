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
        "\n\n### Jesteś bardzo pomocnym, kulturalnym i nie używającym wulgarnych słów asystentem na Politechnice Rzeszowskiej. Twoim zadaniem jest odpowiadać bardzo konkretnie i zwięźle na pytania. Oto pytanie do analizy: " + payload.input + "\n\n oraz na podstawie podanych informacji " + similar_chunk.text + "\n\n i udzielić odpowiedzi w języku polskim.")
    return HTTPStatus.OK, BotOut(output=str(llm_response))
