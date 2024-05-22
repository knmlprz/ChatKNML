import requests

from http import HTTPStatus
from django.http import HttpRequest

from bot.schemas import BotIn, BotOut
from bot.controllers import query_llm_controller

from ninja import Router

router = Router(tags=["Bot"])


@router.post("/bot/", response={HTTPStatus.CREATED: BotOut})
def query_llm(request: HttpRequest, payload: BotIn):
    response = requests.post("0.0.0.0:9000/v1/completions", data=payload)
    return query_llm_controller(response)
