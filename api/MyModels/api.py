from ninja import NinjaAPI

api = NinjaAPI()

api.add_router("/", "MyModels.documents.views.document_router", tags=["Documents"])
api.add_router("/", "MyModels.chunks.views.chunk_router", tags=["Chunks"])
