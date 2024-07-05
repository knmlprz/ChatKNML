from http import HTTPStatus

import requests
from django.db import transaction

from chunks.models import Chunk
from chunks.utils import split_document_into_chunks
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
        print(chunks)
        chunk_instances = []
        for chunk in chunks:
            embeddings_body = {
                "input": chunk.text
            }
            response = requests.post("http://192.168.0.3:9000/v1/embeddings/", json=embeddings_body)
            embedding = response.json()['data'][0]['embedding']
            chunk_instances.append(Chunk(text=chunk.text,
                                         chunk_idx=chunk.chunk_idx,
                                         start_char=chunk.start_char,
                                         end_char=chunk.end_char,
                                         embedding=embedding))
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
        chunk_instances = [Chunk(**chunk) for chunk in chunks]
        Chunk.objects.bulk_create(chunk_instances)
    return document


def delete_document_controller(id: int) -> HTTPStatus:
    document = Document.objects.get(id=id)
    document.delete()
    return HTTPStatus.OK
