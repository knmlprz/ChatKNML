import pytest
from django.test import TestCase
from .models import Chunk


def create_chunk():
    return Chunk.objects.create(
        text="example",
        embedding=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        chunk_idx=1,
        start_char=1,
        end_char=2,
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
        assert (
            Chunk.objects.filter(text="example").exists() == True
        ), "Can't create chunk object"

    @pytest.mark.django_db
    def test_put_method(self):
        create_chunk()
        chunk = Chunk.objects.get(text="example")
        assert (
            Chunk.objects.filter(text="example").exists() == True
        ), "Can't create chunk object"
        chunk.text = "notexample"
        chunk.save()
        assert all(
            a == b for a, b in zip(chunk.embedding, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        ), "Can't update chunk object"

    @pytest.mark.django_db
    def test_delete_method(self):
        create_chunk()
        chunk = Chunk.objects.get(text="example")
        chunk.delete()
        assert (
            Chunk.objects.filter(text="example").exists() == False
        ), "Can't delete chunk object"
