from django.db import models


class Document(models.Model):
    text = models.TextField[str, str]()
