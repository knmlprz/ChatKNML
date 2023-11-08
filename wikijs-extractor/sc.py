from dotenv import load_dotenv
from 

load_dotenv()



llm = OpenAI(
    temperature=0.1, openai_api_key="XD", openai_api_base="http://localhost:8000/v1"
)

query = "Czym jest projekt ChatKNML?"

keywords_chain =  get_extract_keywords_chain(llm=llm)
relevance_chain = get_relevance_chain(llm=llm)

keywords = keywords_chain.invoke({"query": query})


docs = loop.run_until_complete(
    search_by_keywords(session, keywords=keywords, locale="pl")
)

res = loop.run_until_complete(
    asyncio.gather(
        *[
            relevance_chain.ainvoke({"query": query, "document": doc.page_content})
            for doc in docs
        ], return_exceptions=True
    )
)
print(keywords)
print(res)