import dotenv
import chromadb
from langchain.document_loaders import PyPDFDirectoryLoader
from pprint import pprint

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
)
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from chromadb.config import Settings

client = chromadb.HttpClient(settings=Settings(allow_reset=True))
dotenv.load_dotenv()

vectorstore = Chroma(client=client, embedding_function=OpenAIEmbeddings())

# List documents in a directory
loader = PyPDFDirectoryLoader(path="ingest")
documents = loader.load()
print(documents[0].metadata)

# split it into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=20,
    separators=["\r\n", "\r", ".", "?", "!", "\n\n"],
)
docs = text_splitter.split_documents(documents)

pprint(docs)
res = vectorstore.add_documents(docs)
print(res)

query_res = vectorstore.similarity_search("W jaki sposób wziąc urlop na studiach?")
print(query_res)
