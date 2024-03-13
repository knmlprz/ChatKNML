from http import HTTPStatus

from documents.models import Document
from documents.schemas import DocumentIn, DocumentOut


def create_document_controller(payload: DocumentIn) -> tuple[HTTPStatus, DocumentOut]:
    document = Document(**payload.dict())
    document.full_clean()
    document.save()
    return HTTPStatus.CREATED, document


def list_documents_controller() -> list[DocumentOut]:
    return Document.objects.all()


def retrieve_document_controller(id: int) -> DocumentOut:
    document = Document.objects.get(id=id)
    return document


def update_document_controller(payload: DocumentIn, id: int) -> DocumentOut:
    document = Document.objects.get(id=id)
    for attr, value in payload.dict().items():
        setattr(document, attr, value)
    document.full_clean()
    document.save()
    return document


def delete_document_controller(id: int) -> HTTPStatus:
    document = Document.objects.get(id=id)
    document.delete()
    return HTTPStatus.OK
