import os
from enum import Enum
from typing import List, Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from tokenizer import tokenizer
from embedding import embedding
from document_store.elasticsearch import client
from document_store.elasticsearch.es_config import mapping
from config.config import *


es_helper = client.ElasticsearchHelpers(ELASTICSEARCH_URI)

if INIT_INDICES:
    print('\n')
    print("+ Initializing '{INDEX_NAME}' index")
    if USE_DENSE_VECTORS:
        create_index_response = es_helper.create_index(index_name=INDEX_NAME, mapping=mapping.mapping_embedding)
    else:
        create_index_response = es_helper.create_index(index_name=INDEX_NAME, mapping=mapping.mapping_no_embedding)
    
    print('+ Initilization response:\n')
    print('\t', create_index_response)
    print('\n')


print(f'+ Initializing Tokenizers')
regex_tokenizer = tokenizer.RegExTokenizer()
gpt2bpe_tokenizer = tokenizer.GPT2BPETokenizer()
print(f'\t+ Token')

if USE_DENSE_VECTORS:
    print('\n')
    print(f'+ Loading FastText model')
    fasttext_model = embedding.FastTextEmbedding(FASTTEXT_MODEL_PATH)
    print(f"\t+ FastText model '{FASTTEXT_MODEL_PATH.split('/')[-1]}' loaded successfully")

app = FastAPI()

class TokenizerInput(BaseModel):
    urls: List[str]

class EmbedderInput(BaseModel):
    tokens: List[List[str]]

class IndexerInput(BaseModel):
    urls: List[str]

class QueryInput(BaseModel):
    url:str

@app.get('/')
async def homepage():
    return {'HomePage':'!'}

@app.post('/tokenize/{tokenizer_id}')
async def tokenize(tokenizer_id: int, input_urls: TokenizerInput):
    urls = input_urls.urls
    if not urls:
        raise HTTPException(status_code=400, detail="Empty list of URLs")
    if tokenizer_id == 0:
        tokens = regex_tokenizer.tokenize(urls)
        return {
            "tokens": tokens,
            "len": len(tokens)
        }
    elif tokenizer_id == 1:
        tokens = gpt2bpe_tokenizer.tokenize(urls)
        return {
            "tokens": tokens,
            "len": len(tokens)
        }
    else:
        raise HTTPException(status_code=400, detail="Tokenizer does not exist")
    
@app.post('/embedding/{embedder_id}')
async def embedding(embedder_id: int, input_tokens: EmbedderInput):
    if not USE_DENSE_VECTORS:
        raise HTTPException(status_code=400, detail="'USE_DENSE_VECTORS' is set to False")
    tokens = input_tokens.tokens
    if not tokens:
        raise HTTPException(status_code=400, detail="Empty list of Tokens")
    if embedder_id == 0:
        vectors = fasttext_model.get_sentence_vector(tokens).tolist()
        return {
            "vectors": vectors,
            "dim": len(vectors[0]),
            "len": len(vectors)
        }
    else:
        raise HTTPException(status_code=400, detail="Embedder does not exist")

@app.post('/index/{tokenizer_id}/{embedder_id}', status_code=201)
async def index(tokenizer_id: int, embedder_id: int, input_urls: IndexerInput):
    urls = input_urls.urls
    tokens = []
    vectors = []

    if not urls:
        raise HTTPException(status_code=400, detail="Empty list of URLs")

    if tokenizer_id == 0:
        tokens = regex_tokenizer.tokenize(urls)

    elif tokenizer_id == 1:
        tokens = gpt2bpe_tokenizer.tokenize(urls)

    else:
        raise HTTPException(status_code=400, detail="Tokenizer does not exist")

    if not tokens:
        raise HTTPException(status_code=400, detail="Empty list of Tokens")
    
    if USE_DENSE_VECTORS:
        if embedder_id == 0:
            vectors = fasttext_model.get_sentence_vector(tokens).tolist()
        else:
            raise HTTPException(status_code=400, detail="Embedder does not exist")

        if not vectors:
            raise HTTPException(status_code=400, detail="Empty list of Vectors")
    
    bulk_index_res = es_helper.bulk_index(
        index_name=INDEX_NAME,
        urls=urls,
        tokens=tokens,
        embedding=vectors
    )

    is_successful = bulk_index_res['items'][0]['index']['status'] in [200, 201]

    if not is_successful:
        raise HTTPException(status_code=422, detail="Failed Indexing")


@app.post('/query_one_item/{tokenizer_id}/{embedder_id}')
async def query_one_item(tokenizer_id: int, embedder_id: int, q_input:QueryInput):
    url = q_input.url
    urls = [url]
    tokens = []
    vector = []

    if not url:
        raise HTTPException(status_code=400, detail="Empty input")

    if tokenizer_id == 0:
        tokens = regex_tokenizer.tokenize(urls)

    elif tokenizer_id == 1:
        tokens = gpt2bpe_tokenizer.tokenize(urls)

    else:
        raise HTTPException(status_code=400, detail="Tokenizer does not exist")

    if not tokens:
        raise HTTPException(status_code=400, detail="Empty list of Tokens")

    if USE_DENSE_VECTORS:
        if embedder_id == 0:
            vectors = fasttext_model.get_sentence_vector(tokens).tolist()
        else:
            raise HTTPException(status_code=400, detail="Embedder does not exist")

        if not vectors:
            raise HTTPException(status_code=400, detail="Empty list of Vectors")

        vector = vectors[0]

        query_index_res = es_helper.query_index(
            index_name=INDEX_NAME,
            tokens=[],
            embedding=vector,
            only_embedding=True
        )
    else:
        query_index_res = es_helper.query_index(
            index_name=INDEX_NAME,
            tokens=tokens[0],
            only_embedding=False
        )

    if query_index_res:
        return dict(query_index_res)

    raise HTTPException(status_code=422, detail="Query failed")