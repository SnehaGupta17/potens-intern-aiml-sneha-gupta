from src.retrieval import get_retriever

retriever = get_retriever()


question = "What types of leave are available?"
docs = retriever.invoke(question)
for i, doc in enumerate(docs, 1):
    print("=" * 80)
    print(f"Result {i}")
    print("SOURCE:", doc.metadata["source"])
    print("CHUNK:", doc.metadata["chunk_id"])
    print()
    print(doc.page_content)