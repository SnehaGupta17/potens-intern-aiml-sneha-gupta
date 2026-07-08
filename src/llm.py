from dotenv import load_dotenv

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:  # pragma: no cover - optional dependency for tests
    ChatGoogleGenerativeAI = None

# load_dotenv()
import os

load_dotenv(override=True)

print("GOOGLE_API_KEY =", os.getenv("GOOGLE_API_KEY"))

def get_llm():
    if ChatGoogleGenerativeAI is None:
        raise RuntimeError("langchain-google-genai is not installed in the current environment.")

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )