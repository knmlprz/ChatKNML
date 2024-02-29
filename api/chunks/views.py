from http import HTTPStatus
from django.http import HttpRequest

from chunks.models import Chunk
from chunks.schemas import ChunkIn, ChunkOut
from chunks.controllers import *

from ninja import Router
from ninja.pagination import LimitOffsetPagination, paginate

chunk_router = Router(tags=["Chunks"])

@chunk_router.post("/chunk/", response={HTTPStatus.CREATED: ChunkOut})
def create_chunk(request: HttpRequest, payload: ChunkIn):
    http_status, chunk = create_chunk_controller(payload)
    return http_status, chunk

@chunk_router.get("/chunk/", response={HTTPStatus.OK: list[ChunkOut]})
@paginate(LimitOffsetPagination)
def list_chunks(request: HttpRequest):
    chunk = list_chunks_controller()
    return chunk

@chunk_router.get("/chunk/{id}/", response={HTTPStatus.OK: ChunkOut})
def retrieve_chunk(request: HttpRequest, id: int):
    chunk = retrieve_chunk_controller(id)
    return chunk

@chunk_router.put("/chunk/{id}/", response={HTTPStatus.OK: ChunkOut})
def update_chunk(request: HttpRequest, id: int):
    chunk = update_chunk_controller(request,id)
    return chunk

@chunk_router.delete("/chunk/{id}/", response={HTTPStatus.OK: None})
def delete_chunk(request: HttpRequest, id: int):
    http_status = delete_chunk_controller(id)
    return http_status
