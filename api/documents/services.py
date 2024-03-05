import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from db import getdlc

tokenizer = T5Tokenizer.from_pretrained("e5-large-v2")
model = T5ForConditionalGeneration.from_pretrained("e5-large-v2")


def find_similar_documents(
    query_document_text, document_embeddings, documents, top_n=5
):
    inputs = tokenizer.encode(
        "similar documents: " + query_document_text,
        return_tensors="pt",
        max_length=512,
        truncation=True,
    )

    # Generate embeddings for the query
    with torch.no_grad():
        outputs = model(input_ids=inputs)
        query_embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

    document_embeddings = np.frombuffer(document_embeddings, dtype=np.float32).reshape(
        -1, document_embeddings.shape[1]
    )

    similarities = []
    for document_embedding in document_embeddings:
        similarity = cosine_similarity(
            query_embedding.reshape(1, -1), document_embedding.reshape(1, -1)
        )[0][0]
        similarities.append(similarity)

    similar_documents = [(documents[i], similarities[i]) for i in range(len(documents))]
    similar_documents = sorted(similar_documents, key=lambda x: x[1], reverse=True)[
        :top_n
    ]
    return similar_documents


query_document_text = "Pytanie"
document_embeddings, documents = getdlc()

if document_embeddings is not None and documents is not None:
    similar_documents = find_similar_documents(
        query_document_text, document_embeddings, documents
    )
    for document, similarity in similar_documents:
        print(f"Similarity: {similarity}, Document Text: {document}")
else:
    print("Error: Unable to retrieve document embeddings and texts from the database.")
