from django.shortcuts import render
from fastapi import HTTPException, Depends
from fastapi import Router
from django.shortcuts import get_object_or_404
from documents.models import Chunk, Document, WebDocument

router = APIRouter()

@router.post("/chunks/", response_model=Chunk)
async def create_chunk(chunk: ChunkCreate):
    return await Chunk.objects.create(**chunk.dict())

@router.get("/chunks/{chunk_id}", response_model=Chunk)
async def read_chunk(chunk_id: int):
    return await get_object_or_404(Chunk, id=chunk_id)

@router.put("/chunks/{chunk_id}", response_model=Chunk)
async def update_chunk(chunk_id: int, chunk: ChunkCreate):
    db_chunk = await get_object_or_404(Chunk, id=chunk_id)
    for field, value in chunk.dict().items():
        setattr(db_chunk, field, value)
    await db_chunk.save()
    return db_chunk

@router.delete("/chunks/{chunk_id}", response_model=dict)
async def delete_chunk(chunk_id: int):
    chunk = await get_object_or_404(Chunk, id=chunk_id)
    await chunk.delete()
    return {"message": "Chunk deleted successfully"}

@router.post("/documents/", response_model=Document)
async def create_document(document: DocumentCreate):
    chunks_data = document.pop('chunks', [])
    db_document = await Document.objects.create(**document.dict())
    for chunk_data in chunks_data:
        chunk = await Chunk.objects.create(**chunk_data.dict())
        db_document.chunks.add(chunk)
    return db_document

@router.get("/documents/{document_id}", response_model=Document)
async def read_document(document_id: int):
    return await get_object_or_404(Document, id=document_id)

@router.put("/documents/{document_id}", response_model=Document)
async def update_document(document_id: int, document: DocumentCreate):
    db_document = await get_object_or_404(Document, id=document_id)
    chunks_data = document.pop('chunks', [])
    for field, value in document.dict().items():
        setattr(db_document, field, value)
    await db_document.save()
    
    # Usuń stare chunki i dodaj nowe
    db_document.chunks.clear()
    for chunk_data in chunks_data:
        chunk = await Chunk.objects.create(**chunk_data.dict())
        db_document.chunks.add(chunk)
    
    return db_document

@router.delete("/documents/{document_id}", response_model=dict)
async def delete_document(document_id: int):
    document = await get_object_or_404(Document, id=document_id)
    await document.delete()
    return {"message": "Document deleted successfully"}

@router.post("/webdocuments/", response_model=WebDocument)
async def create_webdocument(webdocument: WebDocumentCreate):
    document_data = webdocument.pop('document', {})
    db_document = await Document.objects.create(**document_data.dict())
    db_webdocument = await WebDocument.objects.create(document=db_document, **webdocument.dict())
    return db_webdocument

@router.get("/webdocuments/{webdocument_id}", response_model=WebDocument)
async def read_webdocument(webdocument_id: int):
    return await get_object_or_404(WebDocument, id=webdocument_id)

@router.put("/webdocuments/{webdocument_id}", response_model=WebDocument)
async def update_webdocument(webdocument_id: int, webdocument: WebDocumentCreate):
    db_webdocument = await get_object_or_404(WebDocument, id=webdocument_id)
    document_data = webdocument.pop('document', {})
    
    # Aktualizuj dokument
    db_document = db_webdocument.document
    for field, value in document_data.dict().items():
        setattr(db_document, field, value)
    await db_document.save()

    # Aktualizuj WebDocument
    for field, value in webdocument.dict().items():
        setattr(db_webdocument, field, value)
    await db_webdocument.save()

    return db_webdocument

@router.delete("/webdocuments/{webdocument_id}", response_model=dict)
async def delete_webdocument(webdocument_id: int):
    webdocument = await get_object_or_404(WebDocument, id=webdocument_id)
    await webdocument.delete()
    return {"message": "WebDocument deleted successfully"}
