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



test_data_uni_passau = [

    # 8 path_1=studium
    "https://www.uni-passau.de/studium/",
    "https://www.uni-passau.de/studium/aktuelles/",
    "https://www.uni-passau.de/studium/faq/",
    "https://www.uni-passau.de/studium/vor-dem-studium/",
    "https://www.uni-passau.de/studium/studienabschluss/",
    "https://www.uni-passau.de/studium/campus-und-kultur/",
    "https://www.uni-passau.de/studium/service-und-beratung/",
    "https://www.uni-passau.de/studium/waehrend-des-studiums/",

    # 8 path_1=forschung
    "https://www.uni-passau.de/forschung/",
    "https://www.uni-passau.de/forschung/aktuelles/",
    "https://www.uni-passau.de/forschung/forschungseinrichtungen/",
    "https://www.uni-passau.de/forschung/forschungsfoerderung/",
    "https://www.uni-passau.de/forschung/gute-wissenschaftliche-praxis/",
    "https://www.uni-passau.de/forschung/promotion/",
    "https://www.uni-passau.de/forschung/programme-fuer-gastwissenschaftler/",
    "https://www.uni-passau.de/forschung/wissenschaftspreise/",

    # 7 path_1=wissenstransfer
    "https://www.uni-passau.de/wissenstransfer/",
    "https://www.uni-passau.de/wissenstransfer/aktuelles/",
    "https://www.uni-passau.de/wissenstransfer/trio/",
    "https://www.uni-passau.de/wissenstransfer/kooperationen/",
    "https://www.uni-passau.de/wissenstransfer/gruendungsfoerderung/",
    "https://www.uni-passau.de/wissenstransfer/weiterbildung/",
    "https://www.uni-passau.de/wissenstransfer/technologiemessen/",

    # 6 path_1=internationales
    "https://www.uni-passau.de/internationales/",
    "https://www.uni-passau.de/internationales/aktuelles/",
    "https://www.uni-passau.de/internationales/nach-passau-kommen/",
    "https://www.uni-passau.de/internationales/ins-ausland-gehen/",
    "https://www.uni-passau.de/internationales/internationale-gruppen/",
    "https://www.uni-passau.de/internationales/kontakte/",

    # 6 path_1 = universitaet
    "https://www.uni-passau.de/universitaet/universitaet-im-ueberblick/",
    "https://www.uni-passau.de/universitaet/leitung-und-gremien/",
    "https://www.uni-passau.de/universitaet/fakultaeten/",
    "https://www.uni-passau.de/universitaet/einrichtungen/",
    "https://www.uni-passau.de/universitaet/kontakt/",

    "https://www.uni-passau.de/forschungsdatenmanagement/",
    
    "https://www.uni-passau.de/ethikkommission/",

    "https://www.uni-passau.de/kinect/",

    "https://www.uni-passau.de/studienstart/",
    
    "https://www.uni-passau.de/ringvorlesungen/",

    "https://www.uni-passau.de/welcome-centre/",

    "https://www.uni-passau.de/auslandsamt/",

    "https://www.uni-passau.de/brexit/",
    
    "https://www.uni-passau.de/40-jahre/",

    "https://www.uni-passau.de/adel-in-schlesien/",

    "https://www.uni-passau.de/arbeitskreis-mediensemiotik/",

    "https://www.uni-passau.de/biodiva/",

    "https://www.uni-passau.de/denkmaldigital/",

    "https://www.uni-passau.de/orientierungslauf/",

    "https://www.uni-passau.de/honorswiwi/",
]

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