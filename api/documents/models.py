from django.db import models
from pgvector.django import VectorField
from chunks.models import Chunk
from typing import Tuple

class Document(models.Model):
    text: Tuple[str, str] = models.TextField()
    embedding: Tuple[list[float], VectorField] = VectorField(dimensions=10)
    chunks: Tuple[int, int] = models.ForeignKey(Chunk, on_delete=models.CASCADE, null=True, blank=True)
