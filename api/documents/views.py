from http import HTTPStatus
from typing import List

from django.http import HttpRequest
from ninja import Router
from ninja.pagination import LimitOffsetPagination, paginate

from documents.models import Chunk, Document
from documents.schemas import ChunkIn, ChunkOut, DocumentIn, DocumentOut

router = Router()

@router.post("/chunk/", response={HTTPStatus.CREATED: ChunkOut})
def create_chunk(request: HttpRequest, payload: ChunkIn):
    chunk = Chunk(**payload.dict())
    chunk.full_clean()
    chunk.save()
    return HTTPStatus.CREATED, chunk

@router.get("/chunk/", response={HTTPStatus.OK: List[ChunkOut]})
@paginate(LimitOffsetPagination)
def list_chunks(request: HttpRequest):
    return Chunk.objects.all()

@router.get("/chunk/{id}", response={HTTPStatus.OK: ChunkOut})
def retrieve_chunk(request: HttpRequest, id: int):
    chunk = Chunk.objects.get(id=id)    
    return chunk

@router.put("/chunk/{id}", response={HTTPStatus.OK: ChunkOut})
def update_chunk(request: HttpRequest, id: int, payload: ChunkIn):
    chunk = Chunk.objects.get(id=id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(chunk, attr, value)
    chunk.full_clean()
    chunk.save()
    return chunk

@router.delete("/chunk/{id}", response={HTTPStatus.NO_CONTENT: None})
def delete_chunk(request: HttpRequest, id: int):
    chunk = Chunk.objects.get(id=id)
    chunk.delete()
    return HTTPStatus.NO_CONTENT, None

@router.post("/document/", response={HTTPStatus.CREATED: DocumentOut})
def create_document(request: HttpRequest, payload: DocumentIn):
    document = Document(**payload.dict())
    document.full_clean()
    document.save()
    return HTTPStatus.CREATED, document

@router.get("/document/", response={HTTPStatus.OK: List[DocumentOut]})
@paginate(LimitOffsetPagination)
def list_documents(request: HttpRequest):
    return Document.objects.all()

@router.get("/document/{id}", response={HTTPStatus.OK: DocumentOut})
def retrieve_document(request: HttpRequest, id: int):
    document = Document.objects.get(id=id)    
    return document

@router.put("/document/{id}", response={HTTPStatus.OK: DocumentOut})
def update_document(request: HttpRequest, id: int, payload: DocumentIn):
    document = Document.objects.get(id=id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(document, attr, value)
    document.full_clean()
    document.save()
    return document

@router.delete("/document/{id}", response={HTTPStatus.NO_CONTENT: None})
def delete_document(request: HttpRequest, id: int):
    document = Document.objects.get(id=id)
    document.delete()
    return HTTPStatus.NO_CONTENT, None