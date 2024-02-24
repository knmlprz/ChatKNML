# test_llm.py

import pytest
import requests


def test_llm_response():
    url = 'http://0.0.0.0:9000/v1/completions'
  
    prompt = "co jest stolicą polski?"
    stop_signs = ["\n", "###"]
    data = {
        'prompt': prompt,
        'stop': stop_signs
    }

    response = requests.post(url, json=data)
    
    assert response.status_code == 200
	resp_body = response.json()
    assert 'choices' in resp_body
    assert 'text' in resp_body['choices'][0]
