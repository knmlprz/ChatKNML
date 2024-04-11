from http import HTTPStatus
from django.http import HttpRequest

from chunks.schemas import ChunkIn, ChunkOut
from chunks.controllers import (
    create_chunk_controller,
    list_chunks_controller,
    retrieve_chunk_controller,
    update_chunk_controller,
    delete_chunk_controller,
)


from ninja import Router
from ninja.pagination import LimitOffsetPagination, paginate

router = Router(tags=["Chunks"])


@router.post("/chunk/", response={HTTPStatus.CREATED: ChunkOut})
def create_chunk(request: HttpRequest, payload: ChunkIn):
    return create_chunk_controller(payload)


@router.get("/chunk/", response={HTTPStatus.OK: list[ChunkOut]})
@paginate(LimitOffsetPagination)
def list_chunks(request: HttpRequest):
    return list_chunks_controller()


@router.get("/chunk/{id}/", response={HTTPStatus.OK: ChunkOut})
def retrieve_chunk(request: HttpRequest, id: int):
    return retrieve_chunk_controller(id)


@router.put("/chunk/{id}/", response={HTTPStatus.OK: ChunkOut})
def update_chunk(request: HttpRequest, data: ChunkIn, id: int):
    return update_chunk_controller(data, id)


@router.delete("/chunk/{id}/", response={HTTPStatus.OK: None})
def delete_chunk(request: HttpRequest, id: int):
    return delete_chunk_controller(id)
