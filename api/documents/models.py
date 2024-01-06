from django.db import models
from ninja import ModelSchema
from typing import List
from pydantic import BaseModel

class ChunkBase(BaseModel):
    text: str
    embedding: List[float]
    chunk_idx: int
    start_char_idx: int
    end_char_idx: int

class Chunk(ChunkBase):
    id: int

    class Config:
        orm_mode = True

class DocumentBase(BaseModel):
    text: str
    embedding: List[float]
    chunks: List[ChunkCreate]


class Document(DocumentBase):
    id: int
    chunks: List[Chunk]

    class Config:
        orm_mode = True
