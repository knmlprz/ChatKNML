"""Indexing a directory for chat."""

import argparse
import logging
import sys

from llama_index import (
    ServiceContext,
    SimpleDirectoryReader,
    SimpleKeywordTableIndex,
    StorageContext,
    VectorStoreIndex,
)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

parser = argparse.ArgumentParser(
    prog="Index a directory for chat",
    description="Indexes a directory for chat and outputs a vector store and keyword table",
)
parser.add_argument("input_dir", metavar="input_dir", type=str, help="Input directory")
parser.add_argument(
    "output_dir", metavar="output_dir", type=str, help="Output directory"
)
parser.add_argument("chunk_size", metavar="chunk_size", type=int, help="Chunk size")

args = parser.parse_args()
INPUT_DIR = args.input_dir
PERSIST_DIR = args.output_dir
CHUNK_SIZE = args.chunk_size

# load documents
documents = SimpleDirectoryReader(INPUT_DIR).load_data()

# initialize service context (set chunk size)
service_context = ServiceContext.from_defaults(chunk_size=CHUNK_SIZE)
node_parser = service_context.node_parser

# split documents into nodes (chunks)
nodes = node_parser.get_nodes_from_documents(documents)

# initialize storage context (by default it's in-memory)
storage_context = StorageContext.from_defaults()
storage_context.docstore.add_documents(nodes)

# Create vector embeddings fror nodes
vector_index = VectorStoreIndex(nodes, storage_context=storage_context)

# Extracts keywords from texts using LLM
keyword_index = SimpleKeywordTableIndex(nodes, storage_context=storage_context)

storage_context.persist(PERSIST_DIR)
