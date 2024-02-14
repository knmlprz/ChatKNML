from ninja import Schema
from typing import List

class ChunkIn(Schema):
    text: str
    embedding: List[float]
    chunk_idx: int
    start_char: int
    end_char: int

class ChunkOut(Schema):
    id: int
    text: str
    embedding: List[float]
    chunk_idx: int
    start_char: int
    end_char: int

class DocumentIn(Schema):
    text: str
    embedding: List[float]

class DocumentOut(Schema):
    id: int
    text: str
    embedding: List[float]
