from django.db import models
from pgvector.django import VectorField


class Chunk(models.Model):
    text: str = models.CharField(max_length=100)
    embedding: list[float] = VectorField(dimensions=10)
    chunk_idx: int = models.IntegerField()
    start_char: int = models.IntegerField()
    end_char: int = models.IntegerField()
