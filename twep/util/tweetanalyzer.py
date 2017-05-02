from twep.models import *


class TweetAnalyzer:
    screen_name = None

    def __init__(self, screen_name):
        self.screen_name = screen_name

    def get_most_found_category(self, tweet):
        kws = Keyword.objects.filter(tweets=tweet).filter()