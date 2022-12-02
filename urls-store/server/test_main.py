import os

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"HomePage": "!"}

def test_tokenize_empty_input():
    response = client.post("/tokenize/0", json={"urls": []})
    assert response.status_code == 400
    assert response.json() == {"detail": "Empty list of URLs"}

def test_tokenize_non_existing_tokenizer():
    response = client.post("/tokenize/100", json={"urls": ["https://www.uni-passau.de"]})
    assert response.status_code == 400
    assert response.json() == {"detail": "Tokenizer does not exist"}

def test_tokenize_regex_tokenizer():
    response = client.post("/tokenize/0", json={"urls": ["https://www.uni-passau.de", "https://www.google.de/"]})
    assert response.status_code == 200
    assert response.json() == {
        "tokens": [
            ['https', ':', '/', '/', 'www', '.', 'uni', '-', 'passau', '.', 'de'],
            ['https', ':', '/', '/', 'www', '.', 'google', '.', 'de', '/']
        ],
        "len": 2
    }

def test_tokenize_gpt2bpe_tokenizer():
    response = client.post("/tokenize/1", json={"urls": ["https://www.uni-passau.de", "https://www.google.de/"]})
    assert response.status_code == 200
    assert response.json() == {
        "tokens": [
            ['https', '://', 'www', '.', 'uni', '-', 'pass', 'au', '.', 'de'],
            ['https', '://', 'www', '.', 'google', '.', 'de', '/']
        ],
        "len": 2
    }

def test_embedding_input():
    response = client.post("/embedding/0", json={"tokens": []})
    assert response.status_code == 400
    assert response.json() == {"detail": "Empty list of Tokens"}

def test_embedding_non_existing_embedder():
    response = client.post("/embedding/100", json={"tokens": [["some_token"]]})
    assert response.status_code == 400
    assert response.json() == {"detail": "Embedder does not exist"}

def test_embedding_fasttext_embedder():
    response = client.post("/embedding/0", json={"tokens": [['https', ':', '/', '/', 'www', '.', 'google', '.', 'de', '/'], ["some_token"]]})
    assert response.status_code == 200
    json_res =  response.json()
    json_res_keys = set(json_res.keys())
    assert len(json_res_keys) == 3 and "vectors" in json_res_keys and "dim" in json_res_keys and "len" in json_res_keys, "Wrong output"
    assert len(json_res["vectors"]) == 2 and len(json_res["vectors"][0]) == 300 and len(json_res["vectors"][1]) == 300
    assert json_res["dim"] == 300
    assert json_res["len"] == 2

def test_index():
    #TODO
    pass

def test_query_one_item():
    #TODO
    pass