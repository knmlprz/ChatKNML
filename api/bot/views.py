from http import HTTPStatus

from django.http import HttpRequest
from ninja import Router

from bot.controllers import query_llm_controller
from bot.schemas import BotIn, BotOut, BotError

router = Router(tags=["Bot"])


@router.post("/bot/", response={HTTPStatus.OK: BotOut})
def query_llm(request: HttpRequest, payload: BotIn):
    return query_llm_controller(payload)
