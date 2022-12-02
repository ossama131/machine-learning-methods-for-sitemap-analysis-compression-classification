import unittest
import pickle

from elasticsearch import Elasticsearch

from client import ElasticsearchHelpers
from es_config import mapping

class TestElasticsearchHelpers(unittest.TestCase):

    def test_init_es_connection_working(self):
        es = ElasticsearchHelpers(es_uri="http://localhost:9200")
        self.assertTrue(
            es.client.ping()
        )
    
    def test_init_es_connection_not_working(self):
        not_valid_es_uri = "http://localhost:9220"
        empty_es_uri = ""
        with self.assertRaises(ValueError) as context:
            ElasticsearchHelpers(es_uri=not_valid_es_uri)
        
        self.assertTrue('Connection to elasticsearch failed' in str(context.exception))

        with self.assertRaises(ValueError) as context:
            ElasticsearchHelpers(es_uri=empty_es_uri)

        self.assertTrue('connection string empty' in str(context.exception))

    def test_create_index_non_existing_index(self):
        es = ElasticsearchHelpers(es_uri="http://localhost:9200")
        some_index = "test-index"
        response = es.create_index(some_index, {})
        es.delete_index(some_index)
        self.assertTrue(
            'acknowledged' in response
        )

    def test_create_index_existing_index(self):
        es = ElasticsearchHelpers(es_uri="http://localhost:9200")
        some_index = "test-index-non-existing"
        response_one = es.create_index(some_index, {})
        response_two = es.create_index(some_index, {})
        es.delete_index(some_index)
        self.assertTrue(
            'acknowledged' in response_one and 'error' in response_two
        )

    def test_delete_index_non_existing_index(self):
        es = ElasticsearchHelpers(es_uri="http://localhost:9200")
        some_index = "non-exisitng-test-index"
        response = es.delete_index(some_index)
        self.assertTrue(
            'error' in response
        )

    def test_delete_index_exisiting_index(self):
        es = ElasticsearchHelpers(es_uri="http://localhost:9200")
        some_index = "non-exisitng-test-index"
        response_one = es.create_index(some_index, {})
        response_two = es.delete_index(some_index)
        self.assertTrue(
            'acknowledged' in response_one and 'acknowledged' in response_two
        )

    def test_get_id(self):
        es = ElasticsearchHelpers(es_uri="http://localhost:9200")
        some_url = "http://www.uni-passau.de"
        _id = es._get_id(some_url)
        self.assertEqual(
            _id,
            "18776c0a013e97a549320362a616c87e"
        )

    def test_bulk_index_with_embdding(self):
        with open('test_items/test_urls_50.pkl', 'rb') as f:
            test_urls = pickle.load(f)
        with open('test_items/test_tokens_50.pkl', 'rb') as g:
            test_tokens = pickle.load(g)
        with open('test_items/test_vectors_50.pkl', 'rb') as h:
            test_vectors = pickle.load(h)

        some_index = 'test-index-with-embedding'
        es = ElasticsearchHelpers(es_uri="http://localhost:9200")
        del_index_res = es.delete_index(index_name=some_index)
        new_index_res = es.create_index(index_name=some_index, mapping=mapping.mapping_embedding)
        bulk_index_res = es.bulk_index(
            index_name=some_index,
            urls=test_urls,
            tokens=test_tokens,
            embedding=test_vectors
        )
        del_index_res = es.delete_index(index_name=some_index)
        self.assertTrue(
            len(test_urls) == len(test_tokens) == len(test_vectors) and \
            bulk_index_res['errors'] == False and \
            bulk_index_res['items'][0]['index']['status'] == 201
        )

    def test_bulk_index_without_embedding(self):
        with open('test_items/test_urls_50.pkl', 'rb') as f:
            test_urls = pickle.load(f)
        with open('test_items/test_tokens_50.pkl', 'rb') as g:
            test_tokens = pickle.load(g)

        some_index = 'test-index-without-embedding'
        es = ElasticsearchHelpers(es_uri="http://localhost:9200")
        del_index_res = es.delete_index(index_name=some_index)
        new_index_res = es.create_index(index_name=some_index, mapping=mapping.mapping_no_embedding)
        bulk_index_res = es.bulk_index(
            index_name=some_index,
            urls=test_urls,
            tokens=test_tokens
        )
        del_index_res = es.delete_index(index_name=some_index)
        self.assertTrue(
            len(test_urls) == len(test_tokens) and \
            bulk_index_res['errors'] == False and \
            bulk_index_res['items'][0]['index']['status'] == 201
        )

    def test_bulk_index_with_embedding_different_size_tokens_and_vectors(self):
        with open('test_items/test_urls_50.pkl', 'rb') as f:
            test_urls = pickle.load(f)
        with open('test_items/test_tokens_50.pkl', 'rb') as g:
            test_tokens = pickle.load(g)
        with open('test_items/test_vectors_50.pkl', 'rb') as h:
            test_vectors = pickle.load(h)

        some_index = 'test-index-with-embedding'
        es = ElasticsearchHelpers(es_uri="http://localhost:9200")
        del_index_res = es.delete_index(index_name=some_index)
        new_index_res = es.create_index(index_name=some_index, mapping=mapping.mapping_embedding)
        with self.assertRaises(AssertionError) as context:
            bulk_index_res = es.bulk_index(
                index_name=some_index, 
                urls=test_urls,
                tokens=test_tokens, 
                embedding=test_vectors[:-1]
            )
        
        self.assertTrue(
            'Size of URLs list != Size of Embedding list' in str(context.exception)
        )
        
        del_index_res = es.delete_index(index_name=some_index)

    def test_bulk_index_with_embedding_different_size_urls_and_tokens(self):
        with open('test_items/test_urls_50.pkl', 'rb') as f:
            test_urls = pickle.load(f)
        with open('test_items/test_tokens_50.pkl', 'rb') as g:
            test_tokens = pickle.load(g)

        some_index = 'test-index-without-embedding'
        es = ElasticsearchHelpers(es_uri="http://localhost:9200")
        del_index_res = es.delete_index(index_name=some_index)
        new_index_res = es.create_index(index_name=some_index, mapping=mapping.mapping_no_embedding)
        with self.assertRaises(AssertionError) as context:
            bulk_index_res = es.bulk_index(
                index_name=some_index, 
                urls=test_urls,
                tokens=test_tokens[:-1], 
            )
        
        self.assertTrue(
            'Size of URLs != Size of Tokens' in str(context.exception)
        )
        
        del_index_res = es.delete_index(index_name=some_index)

    def test_query_index(self):
        #TODO
        #test for different cases
        pass