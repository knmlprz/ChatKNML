from django.test import TestCase
from .models import Document

def create_document():
    return Document.objects.create(text="example", embedding=[1,2,3,4,5,6,7,8,9,10])

class DocumentModelTests(TestCase):
    def test_get_method(self):
        response = self.client.get("/api/document/")
        self.assertEqual(response.status_code, 200)

    def test_post_method(self):
        create_document()
        document = Document.objects.get(text="example")
        self.assertEqual(document.text, "example")
        self.assertTrue(Document.objects.filter(text="example").exists())

    def test_put_method(self):
        create_document()
        document = Document.objects.get(text="example")
        document.text = "notexample"
        document.save()
        self.assertEqual(document.text, "notexample")
        self.assertTrue(Document.objects.filter(text="notexample").exists())
        self.assertTrue(all(a == b for a, b in zip(document.embedding, [1,2,3,4,5,6,7,8,9,10])))

    def test_delete_method(self):
        create_document()
        document = Document.objects.get(text="example")
        document.delete()
        self.assertFalse(Document.objects.filter(text="example").exists())
