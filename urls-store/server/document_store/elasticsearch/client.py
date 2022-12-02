import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

import hashlib
from typing import List

from elasticsearch import Elasticsearch
import numpy as np

from es_config import mapping, query_templates

class ElasticsearchHelpers:
    def __init__(self, es_uri:str):
        self.es = self._init_es_connection(es_uri)

    def _init_es_connection(self, es_uri:str) -> Elasticsearch:
        if not es_uri:
            raise ValueError('connection string empty')
            
        es = Elasticsearch(hosts=[es_uri])

        if not es.ping():
            raise ValueError("Connection to elasticsearch failed")

        return es

    @property
    def client(self):
        return self.es

    def __del__(self):
        #close elasticsearch connection if exists
        if hasattr(self, "es"):
            self.es.close()

    def create_index(self, index_name: str, mapping:dict) -> dict:
        response = self.es.indices.create(
            index=index_name,
            body=mapping,
            ignore=400 # ignore 400 already exists code
        )

        return dict(response)

    def delete_index(self, index_name:str) -> dict:
        response = self.es.indices.delete(
            index=index_name,
            ignore=404 # ignore when index is not there
        )

        return dict(response)

    def _get_id(self, url:str) -> str:
        return hashlib.md5(url.encode('utf-8')).hexdigest()


    def bulk_index(self, index_name:str, urls:List[str], tokens:List[List[str]], embedding:np.ndarray = []) -> dict:
        actions = []
        response = {}
        assert len(urls) == len(tokens), "Size of URLs != Size of Tokens"
        if embedding:
            assert len(tokens) == len(embedding) == len(urls), "Size of URLs list != Size of Embedding list"
            for url, token_list, vector in zip(urls, tokens, embedding):
                _id = self._get_id(url)
                url_with_whitespace = " ".join(token_list)
                action = {"index": {"_index": index_name, "_id": _id}}
                doc = {
                    "id": _id,
                    "url": url,
                    "tokens": url_with_whitespace,
                    "embedding": vector
                }

                actions.append(action)
                actions.append(doc)
        else:
            for url, token_list in zip(urls, tokens):
                _id = self._get_id(url)
                url_with_whitespace = " ".join(token_list)
                action = {"index": {"_index": index_name, "_id": _id}}
                doc = {
                    "id": _id,
                    "url": url,
                    "tokens": url_with_whitespace
                }

                actions.append(action)
                actions.append(doc)
        
        if actions:
            response = self.es.bulk(index=index_name, operations=actions)

        return dict(response)

    def query_index(self, index_name:str, tokens: List[str], embedding:np.ndarray = [], only_embedding=False) -> dict:
        response = {}
        if only_embedding:
            assert len(embedding) == mapping.mapping_embedding['mappings']['properties']['embedding']['dims'], "The query vector has a different dimension than the index vectors"
            query_only_embedding_body = query_templates.query_only_embedding(embedding)
            response = self.es.knn_search(
                index=index_name,
                knn = query_only_embedding_body,
                source=['url', 'tokens']
            )

        else:
            url_with_whitespace = " ".join(tokens)
            query_no_embedding_body = query_templates.query_no_embedding(url_with_whitespace)
            response = self.es.search(
                index=index_name,
                body = query_no_embedding_body,
                source=['url', 'tokens']
            )

        return dict(response)