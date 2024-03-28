from ninja import Schema


class DocumentIn(Schema):
    text: str


class DocumentOut(Schema):
    id: int
    text: str
