from http import HTTPStatus

from bot.models import Bot
from bot.schemas import BotIn, BotOut


def query_llm_controller(payload: BotIn) -> tuple[HTTPStatus, BotOut]:
    bot = Bot(**payload.dict())
    return HTTPStatus.CREATED, bot
