from typing import List

from langchain.output_parsers.boolean import BooleanOutputParser
from langchain.prompts import PromptTemplate
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.llms.base import LLM


JUDGE_QUERY_RELEVANCE = """Majac zapytanie i dokument, określ czy dokument może być przedatny dla tego zapytania.

Zapytanie: {query}

Dokument: {document}

Czy dokument jest przydatny? (tak/nie)
"""

EXTRACT_KEYWORDS_PROMPT = """Z danego Zapywania, wyodrębnij najlepsze słowa kluczowe, które można wykorzystać do wyszukiwania. 
1. Uporządkuj je według ważności. 
2. Nie wpisuj niczego poza słowami kluczowymi.
3. Znormalizuj słowa kluczowe.
4. Nie używaj znaków specjalnych.

Zapytanie: {query}
Słowa kluczowe, oddzielone przecinkami:
"""


def get_relevance_chain(
    llm: LLM,
    template=JUDGE_QUERY_RELEVANCE,
    input_variables: List[str] = ["query", "document"],
):
    """Return chain for judging query relevance.
    Chain will take `query` and `document` and return boolean value.

    Args:
        llm: LLM
        prompt: Prompt. Defaults to JUDGE_QUERY_RELEVANCE.

    Returns:
        Chain
    """
    prompt_template = PromptTemplate.from_template(template=template)
    return prompt_template | llm | BooleanOutputParser(false_val="nie", true_val="tak")


def get_extract_keywords_chain(llm: LLM, template=EXTRACT_KEYWORDS_PROMPT):
    prompt_template = PromptTemplate.from_template(template=template)
    return prompt_template | llm | CommaSeparatedListOutputParser()
