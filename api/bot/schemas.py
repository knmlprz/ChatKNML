from ninja import Schema


class BotIn(Schema):
    input: str


class BotOut(Schema):
    output: str


class BotError(Schema):
    pass