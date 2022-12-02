import os
import json
import argparse
import errno
from typing import List
import requests

import config

def validate_config_file(file_path:str):
    #TODO
    #to validate structure and content
    pass

def parse_arguments():
    
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--config_file',
        dest='config_file',
        metavar='config_file',
        required=True,
        type=str,
        help="config file"
    )

    parser.add_argument(
        '--action',
        dest='action',
        choices=['index', 'query', 'tokenize', 'embed'],
        metavar='action',
        required=True,
        type=str,
        help="action to be executed on the server side"
    )

    parser.add_argument(
        '--input_file',
        dest='input_file',
        metavar='input_file',
        required=False,
        default='',
        type=str,
        help="The input file with urls"
    )

    parser.add_argument(
        '--query_text',
        dest='query_text',
        metavar='query_text',
        default='',
        required=False,
        type=str,
        help="The text to be queried"
    )

    parser.add_argument(
        '--only_urls',
        dest='only_urls',
        action='store_true',
        required=False,
        help="Show only results URLs of the query"
    )


    args = parser.parse_args()

    if args.action == 'index' and not args.input_file:
        parser.error('An input file should be provided')

    if args.action == 'query' and not args.query_text:
        parser.error('A query text should be provided')

    return args.config_file, args.action, args.input_file, args.query_text, args.only_urls

def read_file(file_path: str, batch_size:int = 1000):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)
    urls = []
    with open(file_path, 'r', encoding='UTF-8') as f:
        for line in f:
            url = line.strip()
            if url:
                if len(urls) < batch_size:
                    urls.append(url)
                else:
                    yield urls
                    urls = [url]
    if urls:
        yield urls


def validate_config_file(config_file:str) -> bool:
    #TODO
    pass

def index_urls(urls: List[str]) -> bool:
    indexer_config = config.indexer_config
    uri = indexer_config['indexer_uri']
    urls_json = {"urls": urls}

    res = requests.post(uri, json=urls_json)
    is_successful = res.status_code == 201

    return is_successful

def query_one_item(url: str) -> dict:
    query_config = config.query_config
    uri = query_config['query_uri']
    url_json = {"url": url}

    res = requests.post(uri, json=url_json)

    return res.text