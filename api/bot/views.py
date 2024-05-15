from http import HTTPStatus
from dnajgo.http import HttpRequest

from bot.schemas import BotIn, BotOut
from bot.models import Bot

from ninja import Router

router = Router(tags=["Bot"])


@router.post("/bot/", response={HTTPStatus.CREATED: BotOut})
def query_llm(request: HttpRequest, payload: BotIn):
    return query_llm_controller(payload)
