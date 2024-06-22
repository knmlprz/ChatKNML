from itertools import islice

from documents.models import Document
from pydantic import BaseModel


class ChunkData(BaseModel):
    text: str
    chunk_idx: int
    start_char: int
    end_char: int
    document_idx: int


def split_document_into_chunks(
    document: Document, chunk_size: int = 100
) -> list[ChunkData]:
    """Splits document into chunks of size chunk_size and returns them as ChunkData objects."""

    def batched(iterable, n):
        if n < 1:
            raise ValueError('n must be at least one')
        iterable = iter(iterable)
        while batch := tuple(islice(iterable, n)):
            yield batch

    chunks = []
    start_char = 0

    for i, chunk in enumerate(batched(document.text, chunk_size)):
        next_start_char = start_char + len(chunk)

        #TODO: Embedingi i celary job
        chunks.append(
            ChunkData(
                text="".join(chunk),
                chunk_idx=i,
                start_char=start_char,
                end_char=next_start_char - 1,
                document_idx=document.id,
            )
        )

        start_char = next_start_char

    return chunks
