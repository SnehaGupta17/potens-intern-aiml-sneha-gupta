import os
from src.translator import (
    detect_language,
    translate_to_english,
    translate_from_english
)
try:
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser
except ImportError:  # pragma: no cover - optional dependency for tests
    PromptTemplate = None
    StrOutputParser = None

from src.prompts import RAG_PROMPT


retriever = None
llm = None


def _get_retriever():
    global retriever
    if retriever is None:
        from src.retrieval import get_retriever

        retriever = get_retriever()

    return retriever


def _get_llm():
    global llm
    if llm is None:
        from src.llm import get_llm

        llm = get_llm()

    return llm


def _normalize_name(name):
    return os.path.basename(str(name)).strip().lower()


def build_citations(docs, used_docs=None):
    """Build citation objects with source, page/chunk, and snippet."""

    citations = []
    used_names = {
        _normalize_name(doc_name)
        for doc_name in (used_docs or [])
        if doc_name
    }

    for doc in docs:
        source = os.path.basename(str(doc.metadata.get("source", ""))) or "Unknown source"
        page = int(doc.metadata.get("page", 0)) + 1
        chunk = doc.metadata.get("chunk_id")

        if used_names and _normalize_name(source) not in used_names:
            continue

        snippet = (doc.page_content or "").strip()
        if len(snippet) > 280:
            snippet = snippet[:277].rstrip() + "..."

        citations.append(
            {
                "source": source,
                "page": page,
                "chunk": chunk,
                "snippet": snippet,
            }
        )

    if citations:
        return citations

    for doc in docs:
        source = os.path.basename(str(doc.metadata.get("source", ""))) or "Unknown source"
        page = int(doc.metadata.get("page", 0)) + 1
        chunk = doc.metadata.get("chunk_id")
        snippet = (doc.page_content or "").strip()
        if len(snippet) > 280:
            snippet = snippet[:277].rstrip() + "..."

        citations.append(
            {
                "source": source,
                "page": page,
                "chunk": chunk,
                "snippet": snippet,
            }
        )

    return citations


def prepare_rag_inputs(question: str):
    """Translate non-English questions to English for retrieval and record the source language."""

    language = detect_language(question).strip().title()
    retrieval_question = question

    if language and language.lower() not in {"english", "en"}:
        retrieval_question = translate_to_english(question)

    return question, retrieval_question, language


def parse_response(response: str):
    """
    Parse Gemini response into:
    - answer
    - documents used
    - evidence
    """

    answer = ""
    documents = []
    evidence = ""

    section = None

    for line in response.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("Answer:"):
            section = "answer"
            answer = line.replace("Answer:", "").strip()
            continue

        if line.startswith("Documents Used:"):
            section = "documents"
            docs = line.replace("Documents Used:", "").strip()

            if docs:
                documents = [d.strip() for d in docs.split(",")]

            continue

        if line.startswith("Evidence:"):
            section = "evidence"
            continue

        if section == "answer":
            answer += " " + line

        elif section == "documents":

            if line:
                documents.extend(
                    [d.strip() for d in line.split(",")]
                )

        elif section == "evidence":

            line = line.lstrip("-").strip()

            if line:
                evidence += line + " "

    return answer.strip(), documents, evidence.strip()


def ask_question(question: str):

    retriever = _get_retriever()
    llm = _get_llm()

    if PromptTemplate is None or StrOutputParser is None:
        raise RuntimeError("LangChain is not installed in the current environment.")

    original_question, retrieval_question, language = prepare_rag_inputs(question)
    docs = retriever.invoke(retrieval_question)

    context_parts = []

    for doc in docs:

        source = os.path.basename(doc.metadata["source"])
        page = doc.metadata["page"] + 1
        chunk = doc.metadata["chunk_id"]

        context_parts.append(
            f"""
Source: {source}
Page: {page}
Chunk: {chunk}

Content:
{doc.page_content}
"""
        )

    context = "\n\n--------------------------------------------\n\n".join(
        context_parts
    )

    prompt = PromptTemplate.from_template(RAG_PROMPT)

    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    response = chain.invoke(
        {
            "context": context,
            "question": retrieval_question
        }
    )

    answer, used_docs, evidence = parse_response(response)

    if language and language.lower() not in {"english", "en"}:
        answer = translate_from_english(answer, language)

    citations = build_citations(docs, used_docs)

    return {
        "answer": answer,
        "documents_used": used_docs or [citation["source"] for citation in citations],
        "citations": citations
    }