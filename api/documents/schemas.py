from ninja import Schema


class DocumentIn(Schema):
    text: str
    embedding: list[float]


class DocumentOut(Schema):
    id: int
    text: str
    embedding: list[float]
