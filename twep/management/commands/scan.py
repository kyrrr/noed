from django.core.management.base import BaseCommand
from twep.models import MyTweet, Situation, Keyword
from twep.util import tweettransformer
import twep.keywords


# scans through MyTweets by screen_username and formats data
# intention is to use as cronjob in conjunction with getting new tweets, see the command get.py
# TODO: make sure no race conditions??

class Command(BaseCommand):

    help = 'Scans tweet text for EMERGENCIES!!!'
    kws = twep.keywords.kws

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)

    def handle(self, *args, **options):
        sn = options['screen_name']
        print("Scan tweets by " + sn)
        tr = tweettransformer.TweetTransformer(sn)
        tr.set_parent_child()
        tr.make_situation()
        tr.location_scan("oslo")
        for cat in self.kws:
            tr.scan(cat)

