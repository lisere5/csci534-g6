import os
import pathlib

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

_client = None

PROMPT_TEMPLATE = pathlib.Path(__file__).parent.parent / "prompt.txt"


def _get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=os.environ["GROQ_API_KEY"])
    return _client


def _build_prompt(paragraph: str, prior_paragraphs: list[str]) -> str:
    template = PROMPT_TEMPLATE.read_text()
    lines_context = "\n\n".join(prior_paragraphs) if prior_paragraphs else "None"
    prompt = template.replace("[LINE]", paragraph).replace("[LINES]", lines_context)
    return prompt


def adapt_with_llm(paragraph: str, prior_paragraphs: list[str]) -> str:
    prompt = _build_prompt(paragraph, prior_paragraphs)
    response = _get_client().chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()
