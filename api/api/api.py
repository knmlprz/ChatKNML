from ninja import NinjaAPI
from django.urls import path

api = NinjaAPI()

api.add_router("/", "documents.views.router")
api.add_router("/", "chunks.views.router")

urlpatterns = [
    path("api/", api.urls),
]
