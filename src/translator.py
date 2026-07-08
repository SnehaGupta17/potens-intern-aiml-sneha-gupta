try:
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser
except ImportError:  # pragma: no cover - optional dependency for tests
    PromptTemplate = None
    StrOutputParser = None

from src.llm import get_llm

llm = None


def _get_llm():
    global llm
    if llm is None:
        llm = get_llm()
    return llm


def translate_to_english(text: str):

    if PromptTemplate is None or StrOutputParser is None:
        return text

    prompt = PromptTemplate.from_template("""
You are a translator.

Translate the following text into English.

Return ONLY the translated sentence.

Text:
{text}
""")

    chain = prompt | _get_llm() | StrOutputParser()

    return chain.invoke({"text": text})


def translate_from_english(text: str, language: str):

    if PromptTemplate is None or StrOutputParser is None:
        return text

    prompt = PromptTemplate.from_template("""
Translate the following text into {language}.

Return ONLY the translated text.

Text:
{text}
""")

    chain = prompt | _get_llm() | StrOutputParser()

    return chain.invoke(
        {
            "text": text,
            "language": language
        }
    )


def detect_language(text: str):

    prompt = PromptTemplate.from_template("""
Detect the language of the following text.

Return ONLY ONE WORD from these options:

English
Hindi
Marathi

Text:
{text}
""")

    if PromptTemplate is None or StrOutputParser is None:
        return "English"

    chain = prompt | _get_llm() | StrOutputParser()

    return chain.invoke({"text": text}).strip()