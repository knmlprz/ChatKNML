from http import HTTPStatus

import requests
from llama_index.llms.llama_cpp import LlamaCPP
from pgvector.django import L2Distance

from bot.schemas import BotIn, BotOut
from chunks.models import Chunk


def messages_to_prompt(messages):
    prompt = ""
    for message in messages:
        if message.role == 'system':
            prompt += f"<|system|>\n{message.content}</s>\n"
        elif message.role == 'user':
            prompt += f"<|user|>\n{message.content}</s>\n"
        elif message.role == 'assistant':
            prompt += f"<|assistant|>\n{message.content}</s>\n"

    # ensure we start with a system prompt, insert blank if needed
    if not prompt.startswith("<|system|>\n"):
        prompt = "<|system|>\n</s>\n" + prompt

    # add final assistant prompt
    prompt = prompt + "<|assistant|>\n"

    return prompt


def completion_to_prompt(completion):
    return f"<|system|>\n</s>\n<|user|>\n{completion}</s>\n<|assistant|>\n"


def query_llm_controller(payload: BotIn) -> tuple[HTTPStatus, BotOut]:
    # https: // docs.llamaindex.ai / en / stable / api_reference / llms / llama_cpp /
    # TODO: payload na embeding  -> Vector -> Szukamy w bazie podobne -> dokument do payloada
    embeddings_body = {
        "input": payload.input
    }
    response = requests.post("http://192.168.0.3:9000/v1/embeddings/", json=embeddings_body)
    input_embedding = response.json()['data'][0]['embedding']
    similar_chunk = Chunk.objects.order_by(L2Distance('embedding', input_embedding))[0]
    print(similar_chunk.text)
    llm_body = {
        "prompt": "\n\n### Instructions:\nOdpowiedz na pytanie używając 5 zdań" + payload.input + "\n\nWiedząc że" + similar_chunk.text + "\n\n### Response:\n",
        "stop": [
            "\n",
            "###"
        ]
    }
    #llm_response = requests.post("", json=llm_body)
    #llm_response = llm_response.json()['choices'][0]['text']

    model_url = "http://192.168.0.3:9000/v1/completions/"

   # llm = LlamaCPP(
    #    model_url=model_url,
     #   model_path=None,
      #  temperature=0.1,
       # max_new_tokens=256,
        #context_window=3900,
      #  generate_kwargs={},
       # messages_to_prompt=messages_to_prompt,
        #completion_to_prompt=completion_to_prompt,
        #verbose=True,
    #)
    llm_response = "SDS" #llm.complete("Odpowiedz na pytanie używając 5 zdań" + payload.input + "\n\nWiedząc że" + similar_chunk.text)
    return HTTPStatus.OK, BotOut(output=str(llm_response))
