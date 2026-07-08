from types import SimpleNamespace

from src.rag import build_citations


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
