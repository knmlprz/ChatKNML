import pytest
from django.test import TestCase
from documents.models import Document
from .models import Chunk


def create_document():
    return Document.objects.create(
        text="example",
    )


def create_chunk():
    return Chunk.objects.create(
        text="example",
        embedding=list(range(1, 11)),
        chunk_idx=1,
        start_char=1,
        end_char=2,
        document_idx=create_document(),
    )


class ChunkModelTests(TestCase):
    @pytest.mark.django_db
    def test_get_method(self):
        response = self.client.get("/api/chunk/")
        assert (
            response.status_code == 200
        ), "The request could not be received, status code should be 200"

    @pytest.mark.django_db
    def test_post_method(self):
        create_chunk()
        assert Chunk.objects.filter(
            text="example"
        ).exists(), "Can't create chunk object"

    @pytest.mark.django_db
    def test_put_method(self):
        create_chunk()
        chunk = Chunk.objects.get(text="example")
        assert Chunk.objects.filter(
            text="example"
        ).exists(), "Can't create chunk object"
        chunk.text = "notexample"
        chunk.save()
        assert all(
            a == b for a, b in zip(chunk.embedding, range(1, 11))
        ), "Can't update chunk object"

    @pytest.mark.django_db
    def test_delete_method(self):
        create_chunk()
        chunk = Chunk.objects.get(text="example")
        chunk.delete()
        assert not Chunk.objects.filter(
            text="example"
        ).exists(), "Can't delete chunk object"

    @pytest.mark.django_db
    def test_model_foreignkey(self):
        create_chunk()
        document = Document.objects.get(text="example")
        assert Chunk.objects.filter(
            text="example", document_idx=document
        ), "Can't define foreignkey on chunk object"
