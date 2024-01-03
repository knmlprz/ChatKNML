from django.db import models
from django.db import models

# Create your models here.
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

class ChunkCreate(ChunkBase):
    pass

class Chunk(ChunkBase):
    id: int

    class Config:
        orm_mode = True

class DocumentBase(BaseModel):
    text: str
    embedding: List[float]
    chunks: List[ChunkCreate]

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    chunks: List[Chunk]

    class Config:
        orm_mode = True

class WebDocumentCreate(DocumentCreate):
    source: str

class WebDocument(Document):
    source: str

    class Config:
        orm_mode = True
# Create your models here.
