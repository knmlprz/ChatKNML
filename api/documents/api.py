from ninja import NinjaAPI

api = NinjaAPI()

api.add_router("/", "documents.views.document_router", tags=["Documents"])
api.add_router("/", "documents.views.chunk_router", tags=["Chunks"])
