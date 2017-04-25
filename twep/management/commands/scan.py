from django.core.management.base import BaseCommand
from twep.models import MyTweet, Situation, Keyword
from twep.util import tweettransformer


# scans through MyTweets by screen_username and formats data
# intention is to use as cronjob in conjunction with getting new tweets, see the command get_tweets.py
# TODO: make sure no race conditions??

class Command(BaseCommand):

    help = 'Scans tweet text for EMERGENCIES!!!'

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)

    def handle(self, *args, **options):
        sn = options['screen_name']
        tr = tweettransformer.TweetTransformer(sn)
        tr.set_parent_child()
        tr.make_timeline()
        tr.scan('Danger')  # TODO: consts?
        tr.scan('Status')
        tr.scan('Location')
        tr.scan('Actor')
