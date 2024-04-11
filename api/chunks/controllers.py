from http import HTTPStatus

from chunks.models import Chunk
from chunks.schemas import ChunkIn, ChunkOut
from documents.models import Document


def create_chunk_controller(payload: ChunkIn) -> tuple[HTTPStatus, ChunkOut]:
    document_instance = Document.objects.get(pk=payload.document_idx)

    chunk_data = payload.dict()
    chunk_data["document_idx"] = document_instance
    chunk = Chunk(**chunk_data)
    chunk.full_clean()
    chunk.save()
    return HTTPStatus.CREATED, chunk


def list_chunks_controller() -> list[ChunkOut]:
    return Chunk.objects.all()


def retrieve_chunk_controller(id: int) -> ChunkOut:
    chunk = Chunk.objects.get(id=id)
    return chunk


def update_chunk_controller(payload: ChunkIn, id: int) -> ChunkOut:
    document_instance = Document.objects.get(pk=payload.document_idx)

    chunk = Chunk.objects.get(id=id)
    chunk_data = payload.dict()
    chunk_data["document_idx"] = document_instance
    for attr, value in chunk_data.items():
        setattr(chunk, attr, value)
    chunk.full_clean()
    chunk.save()
    return chunk


def delete_chunk_controller(id: int) -> HTTPStatus:
    Chunk.objects.get(id=id).delete()
    return HTTPStatus.OK
