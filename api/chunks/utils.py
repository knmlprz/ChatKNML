from documents.models import Document


def split_document_into_chunks(document: Document, chunk_size: int = 100) -> list[dict]:
    """Splits document into chunks of size chunk_size and returns them as dictionaries.
    End_char is assumed to be the last included character of the document."""
    chunks = []
    start_char = 0
    end_char = chunk_size
    chunk_idx = 1

    while start_char < len(document.text):
        if end_char >= len(document.text):
            end_char = len(document.text)
        chunk_text = document.text[start_char:end_char]
        chunk = dict(
            text=chunk_text,
            chunk_idx=chunk_idx,
            start_char=start_char,
            end_char=(end_char - 1),
            document_idx=document.id,
        )

        chunks.append(chunk)

        start_char += chunk_size
        end_char += chunk_size
        chunk_idx += 1

    return chunks
