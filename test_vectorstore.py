from src.loader import load_documents
from src.chunker import chunk_documents
from src.vectorstore import create_vector_store

documents = load_documents()

chunks = chunk_documents(documents)

vector_store = create_vector_store(chunks)

print("\nVector database created successfully!")