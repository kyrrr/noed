from django.core.management.base import BaseCommand

import twep.keywords
from twep.util.tweets import tweettransformer


# scans through MyTweets by screen_username and formats data
# intention is to use as cronjob in conjunction with getting new tweets, see the command get.py
# TODO: make sure no race conditions??

class Command(BaseCommand):

    help = 'Scans tweet text for EMERGENCIES!!!'
    kws = twep.keywords.kws
    verbose = False

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)
        parser.add_argument('--v', dest='verbose', action='store_true')

    def handle(self, *args, **options):

        if options['verbose']:
            self.verbose = True

        sn = options['screen_name']

        tr = tweettransformer.TweetTransformer(sn, verbose=self.verbose)

        num_rels = tr.set_child_parent()
        print("%s child->parent " % num_rels + "MyTweet relationships set")

        sits = tr.make_timeline()
        print("%s new situations/timelines created" % len(sits))
        tr.location_scan()

        for cat in self.kws:
            tr.scan(cat)
        tr.group_keywords()


