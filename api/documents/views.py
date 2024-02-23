from http import HTTPStatus
from typing import List

from django.http import HttpRequest
from ninja import Router
from ninja.pagination import LimitOffsetPagination, paginate

from documents.models import Document
from documents.schemas import DocumentIn, DocumentOut
import json

document_router = Router()

@document_router.post("/document/", response={HTTPStatus.CREATED: DocumentOut})
def create_document(request: HttpRequest, payload: DocumentIn):
    document = Document(**payload.dict())
    document.full_clean()
    document.save()
    return HTTPStatus.CREATED, document

@document_router.get("/document/", response={HTTPStatus.OK: List[DocumentOut]})
@paginate(LimitOffsetPagination)
def list_documents(request: HttpRequest):
    return Document.objects.all()

@document_router.get("/document/{id}/", response={HTTPStatus.OK: DocumentOut})
def retrieve_document(request: HttpRequest, id: int):
    document = Document.objects.get(id=id)    
    return document

@document_router.put("/document/{id}/", response={HTTPStatus.OK: DocumentOut})
def update_document(request: HttpRequest, id: int):
    document = Document.objects.get(id=id)
    request_data = json.loads(request.body.decode("utf-8"))
    for attr, value in request_data.items():
        setattr(document, attr, value)
    document.full_clean()
    document.save()
    return document

@document_router.delete("/document/{id}/", response={HTTPStatus.OK: None})
def delete_document(request: HttpRequest, id: int):
    document = Document.objects.get(id=id)
    document.delete()
    return HTTPStatus.OK
    