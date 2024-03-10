from django.db import models
from pgvector.django import VectorField


class Chunk(models.Model):
    text = models.CharField[str, str](max_length=100)
    embedding = VectorField[list[float], VectorField](dimensions=10)
    chunk_idx = models.IntegerField[int, int]()
    start_char = models.IntegerField[int, int]()
    end_char = models.IntegerField[int, int]()
