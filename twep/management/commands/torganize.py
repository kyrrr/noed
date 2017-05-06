# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from twep.models import Situation, Keyword, Location, User
from twep.util.text import markdown


# scans through MyTweets by screen_username and formats data
# intention is to use as cronjob in conjunction with getting new tweets, see the command tget.py
# TODO: make sure no race conditions??
from twep.util.tweets import tweettransformer


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)

    def handle(self, *args, **options):
        # get the twitter user name
        sn = options['screen_name']
        try:
            user = User.objects.get(screen_name=sn)
        except User.DoesNotExist:
            print("No user by that name. Try getting tweets first")
            return
        tr = tweettransformer.TweetTransformer(user)
        num_rels = tr.set_child_parent()
        print("%s child->parent " % num_rels + "MyTweet relationships set")
        sits = tr.make_situation()
        print("%s new situations/timelines created" % len(sits))




