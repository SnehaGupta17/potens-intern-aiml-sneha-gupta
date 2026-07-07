import os

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.retrieval import get_retriever
from src.llm import get_llm
from src.prompts import RAG_PROMPT


# Initialize once
retriever = get_retriever()
llm = get_llm()


def ask_question(question: str):
    """
    Retrieve relevant documents, generate an answer using Gemini,
    and return structured citations.
    """

    # Retrieve top matching documents
    docs = retriever.invoke(question)

    # Build context with metadata
    context_parts = []

    for doc in docs:
        source = os.path.basename(doc.metadata["source"])
        page = doc.metadata["page"] + 1
        chunk = doc.metadata["chunk_id"]

        context_parts.append(
            f"""Source: {source}
Page: {page}
Chunk: {chunk}

Content:
{doc.page_content}
"""
        )

    context = "\n\n" + ("-" * 60 + "\n\n").join(context_parts)

    # Create prompt
    prompt = PromptTemplate.from_template(RAG_PROMPT)

    # Create chain
    chain = prompt | llm | StrOutputParser()

    # Generate answer
    answer = chain.invoke(
        {
            "context": context,
            "question": question
        }
    )

    # Build citations
    citations = []

    for doc in docs:
        citations.append(
            {
                "source": os.path.basename(doc.metadata["source"]),
                "page": doc.metadata["page"] + 1,
                "chunk": doc.metadata["chunk_id"],
                "snippet": (
                    doc.page_content[:200] + "..."
                    if len(doc.page_content) > 200
                    else doc.page_content
                ),
            }
        )

    return answer, citations