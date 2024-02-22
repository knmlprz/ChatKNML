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
    assert 'choices' in response.json()
    assert len(response.json()['choices']) > 0
    assert 'text' in response.json()['choices'][0]
