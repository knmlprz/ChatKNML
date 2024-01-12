from django.contrib import admin
from .models import Document, Chunk

admin.site.register(Chunk)
admin.site.register(Document)
