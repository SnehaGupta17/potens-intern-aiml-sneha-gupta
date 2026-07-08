import os

from src.loader import load_documents
from src.llm import get_llm
import json
llm = get_llm()


def check_contradiction(doc1_name, doc2_name):

    docs = load_documents()

    text1 = ""
    text2 = ""

    for doc in docs:

        filename = os.path.basename(doc.metadata["source"])

        if filename == doc1_name:
            text1 += doc.page_content + "\n"

        elif filename == doc2_name:
            text2 += doc.page_content + "\n"

    if text1 == "":
        return {"error": f"{doc1_name} not found"}

    if text2 == "":
        return {"error": f"{doc2_name} not found"}

    prompt = f"""
    You are comparing two company policy documents.

    Document A = {doc1_name}
    Document B = {doc2_name}

    Determine whether these two documents contain any contradictory statements.

    Rules:
    1. If they contradict each other, return ONLY valid JSON.
    2. In the reason field, ALWAYS mention the actual document filenames instead of saying "Document A" or "Document B".
    3. Explain exactly which statements conflict.

    If they conflict, return:

    {{
        "conflict": true,
        "topic": "<policy topic>",
        "reason": "<Explain the contradiction by mentioning {doc1_name} and {doc2_name}>"
    }}

    If they do NOT conflict, return:

    {{
        "conflict": false,
        "reason": "No contradiction found between {doc1_name} and {doc2_name}. These documents cover different policies and do not contain conflicting statements."
    }}

    ========================
    {doc1_name}
    ========================

    {text1}

    ========================
    {doc2_name}
    ========================

    {text2}
    """

    

    response = llm.invoke(prompt)

    content = response.content.strip()

    # Remove markdown formatting if Gemini adds it
    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    # Convert JSON string to Python dictionary
    return json.loads(content)