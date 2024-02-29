from http import HTTPStatus
from django.http import HttpRequest

from documents.models import Document
from documents.schemas import DocumentIn, DocumentOut
from documents.controllers import *

from ninja import Router
from ninja.pagination import LimitOffsetPagination, paginate

document_router = Router(tags=["Documents"])

@document_router.post("/document/", response={HTTPStatus.CREATED: DocumentOut})
def create_document(request: HttpRequest, payload: DocumentIn):
    http_status, document = create_document_controller(payload)
    return http_status, document
    
@document_router.get("/document/", response={HTTPStatus.OK: list[DocumentOut]})
@paginate(LimitOffsetPagination)
def list_documents(request: HttpRequest):
    document = list_documents_controller()
    return document

@document_router.get("/document/{id}/", response={HTTPStatus.OK: DocumentOut})
def retrieve_document(request: HttpRequest, id: int):
    document = retrieve_document_controller(id)
    return document

@document_router.put("/document/{id}/", response={HTTPStatus.OK: DocumentOut})
def update_document(request: HttpRequest, id: int):
    document = update_document_controller(request,id)
    return document

@document_router.delete("/document/{id}/", response={HTTPStatus.OK: None})
def delete_document(request: HttpRequest, id: int):
    http_status = delete_document_controller(id)
    return http_status
