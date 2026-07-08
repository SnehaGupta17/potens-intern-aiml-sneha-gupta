from fastapi import FastAPI
from pydantic import BaseModel
from src.contradiction import check_contradiction
from src.rag import ask_question

app = FastAPI(
    title="RAG Document QA API",
    version="1.0"
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "RAG API is running!"
    }


@app.post("/ask")
def ask(request: QuestionRequest):

    # answer, citations = ask_question(request.question)

    # return {
    #     "question": request.question,
    #     "answer": answer,
    #     "citations": citations
    # }
    result = ask_question(request.question)

    return result

class CompareRequest(BaseModel):
    doc1: str
    doc2: str

@app.post("/contradict")
def contradict(request: CompareRequest):

    result = check_contradiction(
        request.doc1,
        request.doc2
    )

    return result