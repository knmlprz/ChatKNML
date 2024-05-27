import requests

from http import HTTPStatus
from django.http import HttpRequest
from pgvector.django import L2Distance

from bot.schemas import BotIn, BotOut
from bot.controllers import query_llm_controller
from chunks.models import Chunk
from ninja import Router

router = Router(tags=["Bot"])


@router.post("/bot/", response={HTTPStatus.CREATED: BotOut})
def query_llm(request: HttpRequest, payload: BotIn):
    # TODO: payload na embeding  -> Vector -> Szukamy w bazie podobne -> dokument do payloada
    response = requests.post("http://192.168.0.3:9000/v1/embeddings", data=payload.text)

    if not response.ok:
        return HTTPStatus.INTERNAL_SERVER_ERROR

    print(response.content)

   # Chunk.objects.order_by(L2Distance('embedding', response))
    response = requests.post("0.0.0.0:9000/v1/completions", data=payload)
    return query_llm_controller(response)
