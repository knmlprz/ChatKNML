from django.db import models


class Bot(models.Model):
    text = models.TextField[str, str]()
