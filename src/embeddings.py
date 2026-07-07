from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_model():
    """
    Returns the embedding model used throughout the project.
    """

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )