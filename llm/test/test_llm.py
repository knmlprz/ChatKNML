# test_llm.py

import pytest
import requests

# Funkcja do testowania odpowiedzi z API LLM
def test_llm_response():
    # Adres URL lokalnego API LLM w kontenerze Docker
    url = 'http://0.0.0.0:9000/v1/completions'
    
    # Dane do wysłania w zapytaniu
    prompt = "co jest stolicą polski?"
    stop_signs = ["\n", "###"]
    data = {
        'prompt': prompt,
        'stop': stop_signs
    }

    # Wysłanie zapytania do lokalnego API LLM
    response = requests.post(url, json=data)
    
    # Sprawdzenie, czy odpowiedź jest poprawna
    assert response.status_code == 200
    assert 'choices' in response.json()
    assert len(response.json()['choices']) > 0
    assert 'text' in response.json()['choices'][0]
