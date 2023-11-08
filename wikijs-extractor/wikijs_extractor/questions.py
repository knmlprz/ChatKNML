# Generate question from a given documents
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains.llm import LLMChain

from pathlib import Path
from dotenv import load_dotenv
from wikijs_extractor.loaders import load_xslx_to_documents

from pprint import pprint

load_dotenv()

prompt_template = """Wygeneruj podsumowanie poniższego tekstu. A następnie na jego podstawie wygeneruj pytania do tekstu.
Zasady:
1. Pytanie NIE mogą zawierać linków do innych stron
2. Pytania NIE mogą być cytatami z tekstu.
3. Pytania NIE mogą dotyczyć linków do innych stron
4. Pytając o wydarzenia, np. prezentacje, konferencje. MUSISZ podać nazwę wydarzenia. Np. "Kiedy odbyła się konferencja XYZ?"
5. Każde z pytań MUSI być niezależne od pozostałych i nie może zawierać informacji z innych pytań.

Każde pytanie powinno być w formacie:
Numer pytania. Treść pytania

Fragment tekstu:
```
{document}
```
Podsumowanie tekstu 
"""
prompt = PromptTemplate(
    template=prompt_template, input_variables=["document"]
)

llm = OpenAI(temperature=0.7, max_tokens=1000)
llm_chain = LLMChain(llm=llm, prompt=prompt)

documents = load_xslx_to_documents(infile=Path("data3.xlsx"))
idx = 3
result = llm_chain(documents[idx].page_content)

pprint("Input:" + documents[idx].page_content)
pprint(result["text"])

