from typing import Literal
from langchain import OpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.agents import Agent, AgentType

search_tool = DuckDuckGoSearchRun()

tools = [
    Tool(
    name='DuckDuckGo Search',
    func= search_tool.run,
    description="Przydatne, gdy trzeba przeprowadzić wyszukiwanie w Internecie, aby znaleźć informacje, których inne narzędzie nie może znaleźć."
    )
]

smol_model_client = OpenAI(
    openai_api_key="XD",
    openai_api_base="http://host.docker.internal:8001/v1",
)

big_model_client = OpenAI(
    openai_api_key="XD",
    openai_api_base="http://host.docker.internal:8000/v1",
)



PREFIX = """Odpowiedz na poniższe pytania najlepiej jak potrafisz. Odpowiadaj wyłącznie w języku polskim. Masz dostęp do następujących narzędzi:"""
FORMAT_INSTRUCTIONS = """Używaj następującego formatu:

Question: pytanie wejściowe, na które musisz odpowiedzieć
Thought: zawsze powinieneś myśleć o tym, co zrobić.
Action: działanie, które należy podjąć, MUSI być jednym z [{tool_names}] np. wikipedia
Action Input: wejście do Action.
Observation: wynik działania
... (ta Thought/Action/Action Input/Observation może powtórzyć się N razy)
Thought: Znam teraz ostateczną odpowiedź
Final Answer: ostateczna odpowiedź na pierwotne pytanie wejściowe"""
SUFFIX = """Zaczynaj!

Question: {input}
Thought:{agent_scratchpad}"""




async def ask_model(question: str, model: Literal["smol", "big"]):
    client = None
    
    match model:
        case "smol":
            client = smol_model_client
        case "big":
            client = big_model_client

    zero_shot_agent = initialize_agent(
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        tools=tools,
        llm=client,
        verbose=True,
        max_iterations=20,
        handle_parsing_errors=True,
        agent_kwargs={
            'prefix':PREFIX,
            'format_instructions':FORMAT_INSTRUCTIONS,
            'suffix':SUFFIX
        }
    )

    response = await zero_shot_agent.ainvoke({"input": question})

    return str(response)
