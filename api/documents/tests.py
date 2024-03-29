import pytest
from django.test import TestCase
from .models import Document


def create_document():
    return Document.objects.create(text="example")


class DocumentModelTests(TestCase):
    @pytest.mark.django_db
    def test_get_method(self):
        response = self.client.get("/api/document/")
        assert (
            response.status_code == 200
        ), "The request could not be received, status code should be 200"

    @pytest.mark.django_db
    def test_post_method(self):
        create_document()
        assert Document.objects.filter(
            text="example"
        ).exists(), "Can't create document object"

    @pytest.mark.django_db
    def test_put_method(self):
        create_document()
        document = Document.objects.get(text="example")
        assert Document.objects.filter(
            text="example"
        ).exists(), "Can't create document object"
        document.text = "notexample"
        document.save()
        assert Document.objects.filter(
            text="notexample"
        ).exists(), "Can't update document object"

    @pytest.mark.django_db
    def test_delete_method(self):
        create_document()
        document = Document.objects.get(text="example")
        document.delete()
        assert not Document.objects.filter(
            text="example"
        ).exists(), "Can't delete document object"
