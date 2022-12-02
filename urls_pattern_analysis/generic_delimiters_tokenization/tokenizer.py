from typing import List
from urllib.parse import urlparse, parse_qs


class Tokenizer:
    def __init__(self, urls:List[str]) -> None:
        self.urls = urls

    def tokenize_url(self, url: str) -> dict:
        '''
        - Parse url into its generic components: scheme, netloc, path, query and fragment
        - Example: 
            - input: 'https://www.fim.uni-passau.de/some_path?a=1&b=2#desc'
            - output: {
                '__scheme__': 'https',
                '__netloc__': 'www.fim.uni-passau.de',
                '__path_0__': ['some_path'],
                'a': ['1'],
                'b': ['2'],
                '__fragment__': ['desc']
            }
        '''

        url = url.lower().strip('/')

        parsed = urlparse(url)

        scheme = parsed.scheme
        netloc = parsed.netloc
        path = parsed.path
        query = parsed.query
        fragment = parsed.fragment
    
        components = {
            '__scheme__': scheme,
            '__netloc__': netloc,
        }

        if fragment:
            components['__fragment__'] = fragment

        if path:
            path_split = path.strip('/').split('/')
            for i,p in enumerate(path_split):
                components[f'__path_{i}__'] = [p]

        if query:
            #parse_qs('') == {}
            #parse_qs('a=v1&b=v2&a=v3') == {'a': ['v1', 'v3'], 'b': ['v2']}
            query_dict = parse_qs(query)
            for k,v in query_dict.items():
                components[k] = [v]

        return components

    def tokenize_and_group_by_subdomain(self):
        '''
        - Split urls by sudomain, tokenize them, and group them first by subdomain and then by tokenization key
        '''
        subdomains = {}
        for url in self.urls:
            tokenized = self.tokenize_url(url)
            subdomain = tokenized['__netloc__'].lstrip('www.')
            del tokenized['__netloc__']
            del tokenized['__scheme__']
            if subdomain in subdomains.keys():
                for k,v in tokenized.items():
                    if k in subdomains[subdomain].keys():
                        subdomains[subdomain][k].extend(v)
                    else:
                        subdomains[subdomain][k] = v

            else:
                subdomains[subdomain] = tokenized
        
        return subdomains

