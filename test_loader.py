from src.loader import load_documents

docs = load_documents()

print("=" * 50)

print(docs[0].page_content[:400])

print("\nMetadata")

print(docs[0].metadata)