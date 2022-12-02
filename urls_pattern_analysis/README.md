# urls-pattern-mining

Given a set of URLs, output regular expressions that describe different components of the URLs.

## Example
### Input:
    test_data = [
    "https://www.example.com/ctattractions-17876002-Austria_Vienna_attractions.html",
    "https://www.example.com/ctattractions-17826402-Austria_Salzburg_attractions.html",
    "https://www.example.com/ctattractions-17682302-Austria_Graz_attractions.html",
    "https://www.example.com/profile-78587305-Austria_Vienna_Belvedere.html",
    "https://www.example.com/profile-78576005-Austria_Salzburg_Dommuseum.html",
    "https://www.example.com/profile-78571605-Austria_Salzburg_Eisnesenwelt.html"
]

### Output
    {
        'example.com':{
            '__path_0__': '^(ctattractions|profile)(\\-)([0-9]+)(\\-)(austria)(_)([a-zA-Z]+)(_)([a-zA-Z]+)(\\.)(html)$'
        }
    }

## Algorithm

![alt text](https://github.com/ossama131/machine-learning-methods-for-sitemap-analysis-compression-classification/blob/main/resources/urls_pattern_analysis_algorithm.PNG?raw=true)
