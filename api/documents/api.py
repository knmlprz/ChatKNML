from ninja import NinjaAPI
from .views import router as documents_router

api = NinjaAPI()


api.add_router("documents", documents_router, tags=["Documents"])