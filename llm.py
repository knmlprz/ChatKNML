import dotenv

from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.vectorstores import SQLiteVSS
from langchain.embeddings import OpenAIEmbeddings

connection = SQLiteVSS.create_connection(db_file="./vss.db")

dotenv.load_dotenv()

vectorstore = SQLiteVSS(
    embedding=OpenAIEmbeddings(),
    table="state_union",
    connection=connection
)
retriever = vectorstore.as_retriever()


template = """
Jesteś asystentem odpowiadającym na pytania. 
Aby odpowiedzieć na pytanie, użyj następujących elementów kontekstu. 
Jeśli nie znasz odpowiedzi, po prostu powiedz, że nie wiesz. 
Użyj maksymalnie trzech zdań i zachowaj zwięzłość odpowiedzi. 
Odpowiadaj wyłącznie używając języka polskiego.

Pytanie: {question} 
Kontekst: {context} 
Odpowiedź:"""
rag_prompt = PromptTemplate.from_template(template)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=300)
chain = RetrievalQAWithSourcesChain.from_llm(
    llm=llm,
    retriever=retriever,
    verbose=True,
    return_source_documents=True,
    question_prompt=rag_prompt,
)
