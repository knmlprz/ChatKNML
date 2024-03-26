from django.db import models
from pgvector.django import VectorField
from chunks.models import Chunk


class Document(models.Model):
    text = models.TextField[str, str]()
    embedding = VectorField[list[float], VectorField](dimensions=10)
    chunks = models.ForeignKey[int, int](
        Chunk, on_delete=models.CASCADE, null=True, blank=True
    )
