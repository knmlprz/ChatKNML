from django.db import models
from pgvector.django import VectorField

class Chunk(models.Model):
    text = models.CharField(max_length=100)
    embedding = VectorField(dimensions=10)
    chunk_idx = models.IntegerField()
    start_char = models.IntegerField()
    end_char = models.IntegerField()
