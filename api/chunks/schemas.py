from ninja import Schema
from documents.schemas import DocumentOut


class ChunkIn(Schema):
    text: str
    embedding: list[float]
    chunk_idx: int
    start_char: int
    end_char: int
    document_idx: int


class ChunkOut(Schema):
    id: int
    text: str
    embedding: list[float]
    chunk_idx: int
    start_char: int
    end_char: int
    document_idx: DocumentOut
