from http import HTTPStatus
from django.http import HttpRequest

from documents.models import Document
from documents.schemas import DocumentIn, DocumentOut

import json
from typing import Tuple


def create_document_controller(payload: DocumentIn) -> Tuple[HTTPStatus, DocumentOut]:
    document = Document(**payload.dict())
    document.full_clean()
    document.save()
    return HTTPStatus.CREATED, document


def list_documents_controller() -> list[DocumentOut]:
    return Document.objects.all()


def retrieve_document_controller(id: int) -> DocumentOut:
    document = Document.objects.get(id=id)
    return document


def update_document_controller(request: HttpRequest, id: int) -> DocumentOut:
    document = Document.objects.get(id=id)
    request_data = json.loads(request.body.decode("utf-8"))
    for attr, value in request_data.items():
        setattr(document, attr, value)
    document.full_clean()
    document.save()
    return document


def delete_document_controller(id: int) -> HTTPStatus:
    document = Document.objects.get(id=id)
    document.delete()
    return HTTPStatus.OK
