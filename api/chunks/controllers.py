from http import HTTPStatus
from django.http import HttpRequest

from chunks.models import Chunk
from chunks.schemas import ChunkIn, ChunkOut

import json
from typing import Tuple

def create_chunk_controller(payload: ChunkIn) -> Tuple[HTTPStatus, ChunkOut]:
    chunk = Chunk(**payload.dict())
    chunk.full_clean()
    chunk.save()
    return HTTPStatus.CREATED, chunk

def list_chunks_controller() -> (list[ChunkOut]):
    return Chunk.objects.all()

def retrieve_chunk_controller(id: int) -> (ChunkOut):
    chunk = Chunk.objects.get(id=id)
    return chunk

def update_chunk_controller(request: HttpRequest, id: int) -> (ChunkOut):
    chunk = Chunk.objects.get(id=id)
    request_data = json.loads(request.body.decode("utf-8"))
    for attr, value in request_data.items():
        setattr(chunk, attr, value)
    chunk.full_clean()
    chunk.save()
    return chunk

def delete_chunk_controller(id: int) -> (HTTPStatus):
    chunk = Chunk.objects.get(id=id)
    chunk.delete()
    return HTTPStatus.OK
