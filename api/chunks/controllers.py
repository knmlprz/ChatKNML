from http import HTTPStatus
from django.http import HttpRequest

from chunks.models import Chunk
from chunks.schemas import ChunkIn, ChunkOut

import json


def create_chunk_controller(payload: ChunkIn) -> tuple[HTTPStatus, ChunkOut]:
    chunk = Chunk(**payload.dict())
    chunk.full_clean()
    chunk.save()
    return HTTPStatus.CREATED, chunk


def list_chunks_controller() -> list[ChunkOut]:
    return Chunk.objects.all()


def retrieve_chunk_controller(id: int) -> ChunkOut:
    chunk = Chunk.objects.get(id=id)
    return chunk


def update_chunk_controller(payload: ChunkIn, id: int) -> ChunkOut:
    chunk = Chunk.objects.get(id=id)
    for attr, value in payload.dict().items():
        setattr(chunk, attr, value)
    chunk.full_clean()
    chunk.save()
    return chunk


def delete_chunk_controller(id: int) -> HTTPStatus:
    Chunk.objects.get(id=id).delete()
    return HTTPStatus.OK
