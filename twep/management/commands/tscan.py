from django.core.management.base import BaseCommand

import twep.keywords
from twep.models import User
from twep.util.tweets import tweettransformer


# scans through MyTweets by screen_username and formats data
# intention is to use as cronjob in conjunction with getting new tweets, see the command tget.py
# TODO: make sure no race conditions??

class Command(BaseCommand):

    help = 'Scans tweet text for EMERGENCIES!!!'
    kws = twep.keywords.kws
    verbose = False

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)

    def handle(self, *args, **options):
        sn = options['screen_name']
        try:
            user = User.objects.get(screen_name=sn)
        except User.DoesNotExist:
            print("No user by that name. Try getting tweets first")
            return
        tr = tweettransformer.TweetTransformer(user)
        tr.location_scan()
        for cat in self.kws:
            tr.scan(cat)

