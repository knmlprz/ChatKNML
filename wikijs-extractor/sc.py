from dotenv import load_dotenv

load_dotenv()

from wikijs_extractor.loaders import WikiJSLoader
import os

wikijs = WikiJSLoader(url="https://wiki.knml.edu.pl", token=os.getenv("WIKIJS_TOKEN"), locale="pl")

docs = wikijs.search_by_keywords(keywords=["chatknml", "projekt"], locale="pl")

from langchain.prompts import PromptTemplate
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.llms.base import LLM

EXTRACT_KEYWORDS_PROMPT = """Z danego Zapywania, wyodrębnij najlepsze słowa kluczowe, które można wykorzystać do wyszukiwania. 
1. Uporządkuj je według ważności. 
2. Nie wpisuj niczego poza słowami kluczowymi.
3. Znormalizuj słowa kluczowe.
4. Nie używaj znaków specjalnych.

Zapytanie: {query}
Słowa kluczowe, oddzielone przecinkami:
"""

def get_extract_keywords_chain(llm: LLM, prompt=EXTRACT_KEYWORDS_PROMPT):
    prompt_template = PromptTemplate.from_template(template=prompt)
    return prompt_template | llm | CommaSeparatedListOutputParser()

from langchain.docstore.document import Document
from langchain.output_parsers.boolean import BooleanOutputParser

JUDGE_QUERY_RELEVANCE = """Majac zapytanie i dokument, określ czy dokument może być przedatny dla tego zapytania.

Zapytanie: {query}

Dokument: {document}

Czy dokument jest przydatny? (tak/nie)
"""

def get_relevance_chain(llm: LLM, prompt=JUDGE_QUERY_RELEVANCE):
    prompt_template = PromptTemplate.from_template(template=prompt)
    return prompt_template | llm | BooleanOutputParser(false_val="nie", true_val="tak")


from langchain.llms import OpenAI

llm = OpenAI(temperature=0.1,
    openai_api_key="XD",
    openai_api_base="http://localhost:8000/v1"
    )

query = "Czym jest projekt ChatKNML?"

relevance_chain = get_relevance_chain(llm=llm)

for doc in docs:
    print(doc.metadata, relevance_chain.invoke({"query": query, "document": doc.page_content}))