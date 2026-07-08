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

Determine whether they contain any contradictory statements.

If they conflict, reply ONLY in this JSON format:

{{
    "conflict": true,
    "topic": "...",
    "reason": "..."
}}

If they do NOT conflict, reply ONLY:

{{
    "conflict": false,
    "reason": "No contradiction found."
}}

Document A ({doc1_name}):

{text1}


Document B ({doc2_name}):

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