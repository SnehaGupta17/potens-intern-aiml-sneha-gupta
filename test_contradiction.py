from src.contradiction import normalize_reason_with_document_names


def test_normalize_reason_with_document_names_replaces_generic_labels():
    reason = "No contradiction found. Document A outlines general ethical conduct, while Document B details specific employee leave policies."

    normalized = normalize_reason_with_document_names(
        reason,
        "01_Code_of_Conduct.pdf",
        "02_Leave_Policy.pdf",
    )

    assert "01_Code_of_Conduct.pdf" in normalized
    assert "02_Leave_Policy.pdf" in normalized
    assert "Document A" not in normalized
    assert "Document B" not in normalized
