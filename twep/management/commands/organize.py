# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from twep.models import Situation, Keyword, Location
from twep.util.text import markdown


# scans through MyTweets by screen_username and formats data
# intention is to use as cronjob in conjunction with getting new tweets, see the command get.py
# TODO: make sure no race conditions??
from twep.util.tweets import tweettransformer


class Command(BaseCommand):

    # help = 'Print stuff by username to a log file using > or >> in terminal'

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)

    # holy fucking loops batman wtf
    # this cannot be healthy
    def handle(self, *args, **options):
        # get the twitter user name
        sn = options['screen_name']
        tr = tweettransformer.TweetTransformer(sn)
        num_rels = tr.set_child_parent()
        print("%s child->parent " % num_rels + "MyTweet relationships set")
        sits = tr.make_situation()
        print("%s new situations/timelines created" % len(sits))




