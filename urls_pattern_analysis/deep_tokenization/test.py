from colorsys import rgb_to_hls
from helpers import Helpers
from algo import  RegExPatternGenerator

h = Helpers()

test_data = [
    "Chaves:Silvio_8=.html",
    "Ugher:Mangabeira_D=.html",
    "Mendes:Sergio.html"
]

test_data_2 = [
    "ctattractions-17876002-Austria_Vienna_attractions.html",
    "ctattractions-17826402-Austria_Salzburg_attractions.html",
    "ctattractions-17682302-Austria_Graz_attractions.html",
    "profile-78587305-Austria_Vienna_Belvedere.html",
    "profile-78576005-Austria_Salzburg_Dommuseum.html",
    "profile-78571605-Austria_Salzburg_Eisnesenwelt.html"
]

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

amazon_data = [
    'discount-amazon-cat-761520-sku-B00006HU-item-xtend_modem_saver_international_xmods0011r_.html',
    'discount-amazon-cat-1205234-sku-B00006B7-item-256mb_pc100_sdram_for_toshiba4600.html',
    'discount-amazon-cat-720576-sku-B0000A1G-item-victorymul_battery_liion_replaces_dell_p_n_53977e_.html',
    'discount-amazon-cat-1205278-sku-B0000U7H-item-ads_tech_usb_2_0_3_1_2in_external_hard_usbx_835_egfs_.html',
    'module-amazon-details-sku-B00064NX.html',
    'module-amazon-details-sku-B0009M0.html',
    'module-amazon-details-sku-B00006B8.html',
    'module-amazon-details-sku-B00064NX.html'
]

#tokens = tokenize('pqsdqds8745qsd&p:5')

def prep(data:list):
    tokens = []
    for url in data:
        t = url.split("/")[3]
        tokens.append(t)
    
    return tokens

data = prep(test_data_uni_passau)

r = RegExPatternGenerator(test_data_2, min_sup=0.7)

p = r.run()

print(p)
