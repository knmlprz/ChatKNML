from ninja import NinjaAPI
from django.urls import path

api = NinjaAPI()

api.add_router("/", "documents.views.document_router", tags=["Documents"])
api.add_router("/", "chunks.views.chunk_router", tags=["Chunks"])

urlpatterns = [
    path("api/", api.urls),
]