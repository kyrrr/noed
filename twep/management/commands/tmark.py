import base64

from django.core.management.base import BaseCommand

from twep.models import Situation, Keyword, Location, User
from twep.util.text import markdown


# scans through MyTweets by screen_username and formats data
# intention is to use as cronjob in conjunction with getting new tweets, see the command tget.py
# TODO: make sure no race conditions??
from twep.util.tweets import tweettransformer


class Command(BaseCommand):

    # help = 'Print stuff by username to a log file using > or >> in terminal'

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)

    # holy fucking loops batman wtf
    # this cannot be healthy
    def handle(self, *args, **options):
        sn = options['screen_name']
        try:
            user = User.objects.get(screen_name=sn)
        except User.DoesNotExist:
            print("No user by that name. Try getting tweets first")
            return
        mark = markdown.MarkDown()
        mark.header_1(user.screen_name)
        situations = Situation.objects.filter(owner=user)
        for sit in situations:
            tweets = sit.first_tweet.get_all_children(include_self=True)
            mark.header_2(sit.first_tweet.twitter_msg_id)
            for t in tweets:
                mark.text(t.text, italic=True)
                md_list = mark.List("Mulig sted:")
                try:
                    l = Location.objects.get(mytweet=t)
                    md_list.unordered_entry(l.sub_district.name).make()
                except Location.DoesNotExist:
                    pass
                try:
                    ftkws = Keyword.objects.filter(tweets=t)
                    kwmdl = mark.List("Keywords:")
                    for kw in ftkws:
                        kwmdl.unordered_entry(kw.category.name)
                        kwmdl.unordered_entry(kw.word, indentation=1)
                    kwmdl.make()
                except Keyword.DoesNotExist:
                    mark.text("No keywords found for " + t.twitter_msg_id)
                    pass
            user.blob_data = mark.md_str
            user.save()


