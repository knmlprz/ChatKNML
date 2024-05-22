from ninja import Schema


class BotIn(Schema):
    text: str


class BotOut(Schema):
    text: str
