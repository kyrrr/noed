import pprint
import inspect


class Scraper:
    # test data
    violation_keywords = ['avskiltes', 'fratas', 'fratatt']
    good_keywords = ['ingen personskade', 'reddet', 'funnet']
    # danger_keywords = ['røykutvikling', 'knivstukket', 'kniv', 'våpen', 'brann', 'stjålet', 'saknet', 'savnet', 'skudd']
    status_keywords = ['melding om', 'er fremme' 'er på stedet', 'på vei til stedet', 'slukket', 'pågrepet', 'i arrest', 'tatt vare på']
    preposition_keywords = ['i', 'på']
    street_keywords = ['veien', 'gate']
    test_tweets = [
        'Melding om en naken mann som løper rundt i Sandakerveien. Vi er på vei for å forsøke å få på han noe klær.',
        'Helgesens gate. Nødetatene rykker ut til en melding om brann.',
        'Brannen er slukket. Ingen personskade.',
        'Mannen er pågrepet og kjøres arresten.',
        'Vi er i området Bølerbakken. Flere meldere har meldt fra om høye smell utendørs. Uvisst hva dette kan være, mulig skudd.'
    ]

    def __init__(self):
        pass

    def scan_category(self, keyword_category, text):
        for kw in keyword_category:
            if kw in text:
                print("dfgdgdfgdfg")