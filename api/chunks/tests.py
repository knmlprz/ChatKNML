from django.test import TestCase
from .models import Chunk

def create_chunk():
    return Chunk.objects.create(text="example", embedding=[1,2,3,4,5,6,7,8,9,10],chunk_idx=1,start_char=1,end_char=2)

class ChunkModelTests(TestCase):
    def test_get_method(self):
        response = self.client.get("/api/chunk/")
        self.assertEqual(response.status_code, 200)

    def test_post_method(self):
        create_chunk()
        chunk = Chunk.objects.get(text="example")
        self.assertEqual(chunk.text, "example")
        self.assertTrue(Chunk.objects.filter(text="example").exists())

    def test_put_method(self):
        create_chunk()
        chunk = Chunk.objects.get(text="example")
        chunk.text = "notexample"
        chunk.save()
        self.assertEqual(chunk.text, "notexample")
        self.assertTrue(Chunk.objects.filter(text="notexample").exists())
        self.assertTrue(all(a == b for a, b in zip(chunk.embedding, [1,2,3,4,5,6,7,8,9,10])))

    def test_delete_method(self):
        create_chunk()
        chunk = Chunk.objects.get(text="example")
        chunk.delete()
        self.assertFalse(Chunk.objects.filter(text="example").exists())
