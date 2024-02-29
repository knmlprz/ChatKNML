from ninja import NinjaAPI
from django.urls import path

api = NinjaAPI()

api.add_router("/", "documents.views.document_router")
api.add_router("/", "chunks.views.chunk_router")

urlpatterns = [
    path("api/", api.urls),
]
