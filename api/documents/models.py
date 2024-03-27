from django.db import models
from pgvector.django import VectorField


class Document(models.Model):
    text = models.TextField[str, str]()
    embedding = VectorField[list[float], VectorField](dimensions=10)
