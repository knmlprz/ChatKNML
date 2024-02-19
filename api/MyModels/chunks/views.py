from http import HTTPStatus
from typing import List

from django.http import HttpRequest
from ninja import Router
from ninja.pagination import LimitOffsetPagination, paginate
from django.shortcuts import get_object_or_404

from MyModels.models import Chunk
from MyModels.chunks.schemas import ChunkIn, ChunkOut
import json

chunk_router = Router()

@chunk_router.post("/chunk/", response={HTTPStatus.CREATED: ChunkOut})
def create_chunk(request: HttpRequest, payload: ChunkIn):
    chunk = Chunk(**payload.dict())
    chunk.full_clean()
    chunk.save()
    return HTTPStatus.CREATED, chunk

@chunk_router.get("/chunk/", response={HTTPStatus.OK: List[ChunkOut]})
@paginate(LimitOffsetPagination)
def list_chunks(request: HttpRequest):
    return Chunk.objects.all()

@chunk_router.get("/chunk/{id}/", response={HTTPStatus.OK: ChunkOut}) 
def retrieve_chunk(request: HttpRequest, id: int):
    chunk = Chunk.objects.get(id=id)  
    return chunk

@chunk_router.put("/chunk/{id}/", response={HTTPStatus.OK: ChunkOut})
def update_chunk(request: HttpRequest, id: int):
    chunk = Chunk.objects.get(id=id)
    request_data = json.loads(request.body.decode("utf-8"))
    for attr, value in request_data.items():
        setattr(chunk, attr, value)
    chunk.full_clean()
    chunk.save()
    return chunk

@chunk_router.delete("/chunk/{id}/", response={HTTPStatus.OK: None})
def delete_chunk(request: HttpRequest, id: int):
    chunk = Chunk.objects.get(id=id)
    chunk.delete()
    return HTTPStatus.OK
