import pprint
import inspect
from twep.settings import KEYWORDS

class Scraper:
    # test data
    violation_keywords = ['avskiltes', 'fratas', 'fratatt']
    good_keywords = ['ingen personskade', 'reddet', 'funnet']
    # danger_keywords = ['røykutvikling', 'knivstukket', 'kniv', 'våpen', 'brann', 'stjålet', 'saknet', 'savnet', 'skudd']
    status_keywords = ['melding om', 'er fremme' 'er på stedet', 'på vei til stedet', 'slukket', 'pågrepet', 'i arrest', 'tatt vare på']
    preposition_keywords = ['i', 'på']
    street_keywords = ['veien', 'gate']

    keywords = None

    def __init__(self):
        self.keywords = KEYWORDS[0]

    # figure out what is to be scanned for in a tweet
    # currently implemented:
    #     danger
    def scan(self, text, category=None):
        if category is None:
            print("scan for all")
            print("scan for all is not yet implemented!!")
            return "Bababa"
        print("scan for " + category)
        return {
            'danger': self.scan_danger(text)
        }[category]

    # match a tweet to the list of spooky bad keywords
    def scan_danger(self, text):
        for dkw in self.keywords['DANGER']:
            if dkw in text:
                print("/!\\DANGER DANGER/!\\")
                print("Found: " + dkw)
                print("In text: ")
                print(text)
        pass
