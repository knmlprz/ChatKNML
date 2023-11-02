import streamlit as st
import argparse
from pathlib import Path
from dotenv import load_dotenv

from wikijs_extractor.loaders import load_xslx_to_documents

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

load_dotenv()

## Parse arguments
parser = argparse.ArgumentParser(description='Chatbot')
parser.add_argument("file", default='data.xslx', type=Path, help='Path to xlsx file')

file = parser.parse_args().file
documents = load_xslx_to_documents(file)

## Load documents into chromadb

docsearch = Chroma.from_documents(documents, OpenAIEmbeddings())

prompt_template = """Użyj poniższych fragmentów kontekstu, aby odpowiedzieć na pytanie na końcu. Jeśli nie znasz odpowiedzi, po prostu powiedz, że nie wiesz, nie próbuj wymyślać odpowiedzi.
Każdy fragment kontekstu może zawierać krótki opis na początku, oraz źródło - ścieżkę do pliku z którego pochodzi.

{context}

Pytanie: {question}
Odpowiedź w języku polskim:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)
chain = load_qa_chain(OpenAI(temperature=0, ), chain_type="stuff", prompt=PROMPT)

## Chat

# Accept user input
if prompt := st.chat_input("Zadaj pytanie?"):
    # Add user message to chat history
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        docs = docsearch.similarity_search(prompt)
        result = chain({"input_documents": docs, "question": prompt}, return_only_outputs=True)
        message_placeholder.markdown(result["output_text"])
        
        st.write(docs)

