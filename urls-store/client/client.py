import json
import sys

import utils
import config

if __name__ == '__main__':

    config_file, action, input_file, query_text, only_urls = utils.parse_arguments()

    #TODO
    #not implemented yet
    utils.validate_config_file(config_file)

    if action == 'index':
        success = 0
        total_urls = 0
        indexer_config = config.indexer_config
        print(f'+ Start Indexing...')
        for urls in utils.read_file(input_file, indexer_config['batch_size']):
            res = utils.index_urls(urls)
            success += int(res) * len(urls)
            total_urls += len(urls)
        print(f'+ {success} out of {total_urls} indexed successfully')
        sys.exit(0)

    if action == 'query':
        res = utils.query_one_item(query_text)
        res = json.loads(res)
        if only_urls:
            for hit in res['hits']['hits']:
                print(hit['_source']['url'])
        else:
            print(json.dumps(res, indent=4))
            
        sys.exit(0)

    if action == 'tokenize':
        raise NotImplementedError("To be implemented")

    if action == 'embed':
        raise NotImplementedError("To be implemented")