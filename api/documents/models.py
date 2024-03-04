from django.db import models
from pgvector.django import VectorField
from chunks.models import Chunk


class Document(models.Model):
    text: str = models.TextField()
    embedding: list[float] = VectorField(dimensions=10)
    chunks: int = models.ForeignKey(
        Chunk, on_delete=models.CASCADE, null=True, blank=True
    )
