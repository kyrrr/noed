from django.core.management.base import BaseCommand
from twep.models import MyTweet, Situation, Keyword
from twep.util import logger
from twep.util import tweettransformer
from collections import defaultdict


# scans through MyTweets by screen_username and formats data
# intention is to use as cronjob in conjunction with getting new tweets, see the command get_tweets.py
# TODO: make sure no race conditions??

class Command(BaseCommand):

    help = 'Scans tweet text for EMERGENCIES!!!'
    # hold log message
    msg = "\n"

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)

    def handle(self, *args, **options):
        sn = options['screen_name']
        s = tweettransformer.TweetTransformer(sn)
        s.set_parent_child()
        s.situate()
        s.scan('Danger')  # TODO: consts?
        s.scan('Status')
        with_danger_keywords = MyTweet.objects.filter(keyword__category='Danger').filter(keyword__category='Status')
        for wdk in with_danger_keywords:
            dk = wdk.keyword.all()
            for k in dk:
                pass
                # print(k.word.encode("UTF-8"))
