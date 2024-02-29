from ninja import Schema

class ChunkIn(Schema):
    text: str
    embedding: list[float]
    chunk_idx: int
    start_char: int
    end_char: int

class ChunkOut(Schema):
    id: int
    text: str
    embedding: list[float]
    chunk_idx: int
    start_char: int
    end_char: int
