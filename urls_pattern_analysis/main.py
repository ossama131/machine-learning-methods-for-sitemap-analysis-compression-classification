from typing import List

from generic_delimiters_tokenization.tokenizer import Tokenizer
from deep_tokenization.algo import RegExPatternGenerator


def get_patterns(urls:List[str], min_sup:float=0.7) -> dict:
    subdomains_regular_expressions = {}

    #init Generic delimiters Tokenizer
    tokenizer = Tokenizer(urls)

    subdomains = tokenizer.tokenize_and_group_by_subdomain()

    for subdomain, d in subdomains.items():
        if subdomain not in subdomains_regular_expressions.keys():
            subdomains_regular_expressions[subdomain] = {}
        
        for k,v in d.items():
            regex_pattern_generator = RegExPatternGenerator(v, min_sup)
            regex_str = regex_pattern_generator.run()
            subdomains_regular_expressions[subdomain][k] = regex_str
    
    return subdomains_regular_expressions

test_data_2 = [
    "https://www.example.com/ctattractions-17876002-Austria_Vienna_attractions.html",
    "https://www.example.com/ctattractions-17826402-Austria_Salzburg_attractions.html",
    "https://www.example.com/ctattractions-17682302-Austria_Graz_attractions.html",
    "https://www.example.com/profile-78587305-Austria_Vienna_Belvedere.html",
    "https://www.example.com/profile-78576005-Austria_Salzburg_Dommuseum.html",
    "https://www.example.com/profile-78571605-Austria_Salzburg_Eisnesenwelt.html"
]

if __name__ == '__main__':
    patterns = get_patterns(test_data_2)
    print(patterns)
