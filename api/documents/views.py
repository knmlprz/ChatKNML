from http import HTTPStatus
from django.http import HttpRequest

from documents.schemas import DocumentIn, DocumentOut
from documents.controllers import (
    create_document_controller,
    list_documents_controller,
    retrieve_document_controller,
    update_document_controller,
    delete_document_controller,
)

from ninja import Router
from ninja.pagination import LimitOffsetPagination, paginate

router = Router(tags=["Documents"])


@router.post("/document/", response={HTTPStatus.CREATED: DocumentOut})
def create_document(request: HttpRequest, payload: DocumentIn):
    return create_document_controller(payload)


@router.get("/document/", response={HTTPStatus.OK: list[DocumentOut]})
@paginate(LimitOffsetPagination)
def list_documents(request: HttpRequest):
    return list_documents_controller()


@router.get("/document/{id}/", response={HTTPStatus.OK: DocumentOut})
def retrieve_document(request: HttpRequest, id: int):
    return retrieve_document_controller(id)


@router.put("/document/{id}/", response={HTTPStatus.OK: DocumentOut})
def update_document(request: HttpRequest, data: DocumentIn, id: int):
    return update_document_controller(data, id)


@router.delete("/document/{id}/", response={HTTPStatus.OK: None})
def delete_document(request: HttpRequest, id: int):
    return delete_document_controller(id)
