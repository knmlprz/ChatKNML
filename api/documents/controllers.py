from http import HTTPStatus

from django.db import transaction
from chunks.utils import split_document_into_chunks
from chunks.models import Chunk
from documents.models import Document
from documents.schemas import DocumentIn, DocumentOut


def create_document_controller(payload: DocumentIn) -> tuple[HTTPStatus, DocumentOut]:
    """Creating the document and chunks of that document.
    Making sure that both chunks and document are created by using atomic transaction.
    """
    with transaction.atomic():
        document = Document(**payload.dict())
        document.full_clean()
        document.save()

        chunks = split_document_into_chunks(document, 100)
        chunk_instances = [Chunk(**chunk_data) for chunk_data in chunks]
        Chunk.objects.bulk_create(chunk_instances)

    return HTTPStatus.CREATED, document


def list_documents_controller() -> list[DocumentOut]:
    return Document.objects.all()


def retrieve_document_controller(id: int) -> DocumentOut:
    document = Document.objects.get(id=id)
    return document


def update_document_controller(payload: DocumentIn, id: int) -> DocumentOut:
    with transaction.atomic():
        document = Document.objects.filter(id=id).update(**payload.dict())
        document.full_clean()
        document.save()

        # Removing old chunks and generating new ones.
        Chunk.objects.filter(chunks__document_idx=document).delete()
        chunks = split_document_into_chunks(document, 100)
        chunk_instances = [Chunk(**chunk_data) for chunk_data in chunks]
        Chunk.objects.bulk_create(chunk_instances)
    return document


def delete_document_controller(id: int) -> HTTPStatus:
    document = Document.objects.get(id=id)
    document.delete()
    return HTTPStatus.OK
