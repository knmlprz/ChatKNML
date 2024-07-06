from django.db import models
from pgvector.django import VectorField
from documents.models import Document


class Chunk(models.Model):
    text = models.CharField[str, str](max_length=1000)
    embedding = VectorField[list[float], VectorField](dimensions=4096)
    chunk_idx = models.IntegerField[int, int]()
    start_char = models.IntegerField[int, int]()
    end_char = models.IntegerField[int, int]()
    document_idx = models.ForeignKey[int, Document](
        Document, on_delete=models.CASCADE, null=True, blank=True
    )
