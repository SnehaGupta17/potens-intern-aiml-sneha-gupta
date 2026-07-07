from src.loader import load_documents
from src.chunker import chunk_documents

# Step 1: Load all documents
documents = load_documents()

# Step 2: Split into chunks
chunks = chunk_documents(documents)

print("=" * 60)

# Total chunks created
print(f"Total Chunks: {len(chunks)}")

print("=" * 60)

# Display the first chunk
print("FIRST CHUNK:\n")
print(chunks[0].page_content)

print("\n" + "=" * 60)

# Display metadata
print("METADATA:\n")
print(chunks[0].metadata)