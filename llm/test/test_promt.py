import requests
import json


def query_local_openai_api(prompt, stop_signs):
    url = "http://127.0.0.1:9000/v1/completions"
    headers = {"Content-Type": "application/json"}
    data = {"prompt": prompt, "stop": stop_signs}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()
    else:
        return response.text


# Prompt and stop_signs
prompt = "\n\n### Instructions:\n jaka jest stolica polski\n\n### Response:\n"
stop_signs = ["\n", "###"]

# Query local API
result = query_local_openai_api(prompt, stop_signs)

print(result["choices"][0]["text"])
