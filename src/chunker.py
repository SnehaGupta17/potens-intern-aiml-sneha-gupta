from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(documents):
    """
    Split documents into smaller chunks while preserving metadata.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=120,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = text_splitter.split_documents(documents)

    # Add chunk ID
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i + 1

    print(f"\nTotal Chunks Created: {len(chunks)}")

    return chunks