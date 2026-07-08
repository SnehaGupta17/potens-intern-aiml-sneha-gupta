from types import SimpleNamespace

from src.rag import build_citations, prepare_rag_inputs


def make_doc(source, page, chunk_id, content):
    return SimpleNamespace(
        metadata={"source": source, "page": page, "chunk_id": chunk_id},
        page_content=content,
    )


def test_build_citations_includes_source_page_chunk_and_snippet():
    docs = [
        make_doc("/tmp/01_Code_of_Conduct.pdf", 0, 1, "Employees must follow company policy."),
        make_doc("/tmp/02_Leave_Policy.pdf", 3, 4, "Full-time employees accrue 20 days of paid vacation annually."),
    ]

    citations = build_citations(docs, ["02_Leave_Policy.pdf"])

    assert len(citations) == 1
    assert citations[0]["source"] == "02_Leave_Policy.pdf"
    assert citations[0]["page"] == 4
    assert citations[0]["chunk"] == 4
    assert "paid vacation" in citations[0]["snippet"]


def test_prepare_rag_inputs_translates_non_english_question(monkeypatch):
    monkeypatch.setattr("src.rag.detect_language", lambda text: "Hindi")
    monkeypatch.setattr("src.rag.translate_to_english", lambda text: "How many paid vacation days do employees receive?")

    original_question, retrieval_question, language = prepare_rag_inputs("कर्मचारियों को कितने छुट्टी के दिन मिलते हैं?")

    assert original_question == "कर्मचारियों को कितने छुट्टी के दिन मिलते हैं?"
    assert retrieval_question == "How many paid vacation days do employees receive?"
    assert language == "Hindi"
