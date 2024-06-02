from http import HTTPStatus

import requests
from pgvector.django import L2Distance

from bot.schemas import BotIn, BotOut
from chunks.models import Chunk


def query_llm_controller(payload: BotIn) -> tuple[HTTPStatus, BotOut]:
    # TODO: payload na embeding  -> Vector -> Szukamy w bazie podobne -> dokument do payloada
    embeddings_body = {
        "input": payload.input
    }
    response = requests.post("http://192.168.0.3:9000/v1/embeddings/", json=embeddings_body)
    input_embedding = response.json()['data'][0]['embedding']
    similar_chunk = Chunk.objects.order_by(L2Distance('embedding', input_embedding))[0]
    print(similar_chunk.text)
    llm_body = {
        "prompt": "\n\n### Instructions:\nOdpowiedz na pytanie "+ payload.input +"\n\nWiedząc że"+similar_chunk.text+"\n\n### Response:\n",
        "stop": [
            "\n",
            "###"
        ]
    }
    llm_response = requests.post("http://192.168.0.3:9000/v1/completions/", json=llm_body)
    llm_response = llm_response.json()['choices'][0]['text']
    return HTTPStatus.OK, BotOut(output=str(llm_response))
