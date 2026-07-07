import os
from langchain_community.document_loaders import PyMuPDFLoader


def load_documents(folder_path="doc"):
    """
    Load all PDF documents from the specified folder.

    Returns:
        List of LangChain Document objects.
    """

    documents = []

    # Iterate through all files
    for filename in os.listdir(folder_path):

        if filename.endswith(".pdf"):

            file_path = os.path.join(folder_path, filename)

            print(f"Loading: {filename}")

            loader = PyMuPDFLoader(file_path)

            docs = loader.load()

            documents.extend(docs)

    print(f"\nTotal Pages Loaded: {len(documents)}")

    return documents