def split_document_into_chunks(document, chunk_size):
    chunks = []
    start_char = 0
    end_char = chunk_size
    chunk_idx = 1

    while start_char < len(document):
        if end_char >= len(document):
            end_char = len(document)
        chunk_text = document[start_char:end_char]
        chunk = {
            'text': chunk_text,
            'chunk_idx': chunk_idx,
            'start_char': start_char,
            'end_char': end_char
        }
        chunks.append(chunk)

        start_char += chunk_size
        end_char += chunk_size
        chunk_idx += 1

    return chunks