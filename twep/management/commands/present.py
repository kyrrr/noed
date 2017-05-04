# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from twep.models import MyTweet, Situation, Keyword, KeywordCategory, Location
from twep.util import markdown
import unicodedata
import sys


# scans through MyTweets by screen_username and formats data
# intention is to use as cronjob in conjunction with getting new tweets, see the command get.py
# TODO: make sure no race conditions??

class Command(BaseCommand):

    # help = 'Print stuff by username to a log file using > or >> in terminal'

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)
        parser.add_argument('category', type=str, nargs="?")

    # holy fucking loops batman wtf
    # this cannot be healthy
    def handle(self, *args, **options):
        # get the twitter user name
        sn = options['screen_name']
        # f = options['category']
        mark = markdown.MarkDown(sn)
        situations = Situation.objects.filter(screen_name=sn)
        for sit in situations:
            first = sit.first_tweet
            mark.header_1(first.twitter_msg_id)\
                .text(first.text)
            try:
                l = Location.objects.get(mytweet=first)
                mark.header_4("Possible location:")\
                    .text(l.sub_district.name)
                # print("#### Possible location:")
                # print(l.sub_district.name)
            except Location.DoesNotExist:
                pass

            try:
                ftkws = Keyword.objects.filter(tweets=first)
                mark.header_4("Keywords:")
                for kw in ftkws:
                    mark.text(kw.word)
            except Keyword.DoesNotExist:
                print("No keywords found for " + first.twitter_msg_id)
                pass
            if sit.children.all().count() > 0:
                # print("### Children texts:")
                for i, sc in enumerate(sit.children.all()):
                    mark.header_4("Follow-up %s:" % (i + 1))
                    mark.text(sc.text)
                    # print(sc.text)
                    try:
                        cl = Location.objects.get(mytweet=sc)

                        mark.header_4("Possible location")\
                            .text(cl.sub_district.name)
                        # print("#### Possible location:")
                        # print(cl.sub_district.name)
                    except Location.DoesNotExist:
                        pass

                    try:
                        ckws = Keyword.objects.filter(tweets=sc)
                        mark.header_4("Keywords:")
                        for ckw in ckws:
                            mark.text(ckw.word)
                    except Keyword.DoesNotExist:
                        print("No keywords found for " + first.twitter_msg_id)
                        pass
                    # if sc.get_last_parent() and sit.first_tweet == sc.get_last_parent():
                        # pass

        mark.save()



