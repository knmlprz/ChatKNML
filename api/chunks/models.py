from django.db import models
from pgvector.django import VectorField
from typing import Tuple

class Chunk(models.Model):
    text: Tuple[str, str] = models.CharField(max_length=100)
    embedding: Tuple[list[float], VectorField] = VectorField(dimensions=10)
    chunk_idx: Tuple[int, int] = models.IntegerField()
    start_char: Tuple[int, int] = models.IntegerField()
    end_char: Tuple[int, int] = models.IntegerField()
