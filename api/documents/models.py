from django.db import models


class Chunk(models.Model):
    text = models.CharField(max_length=100)
    # TODO: Change this
    embedding = models.CharField(max_length=100)
    chunk_idx = models.IntegerField()
    start_char = models.IntegerField()
    end_char = models.IntegerField()


class Document(models.Model):
    text = models.TextField()
    embedding = models.CharField(max_length=100)
    chunks = models.ForeignKey(Chunk, on_delete=models.CASCADE)
