from django.core.management.base import BaseCommand
from twep.models import MyTweet, Situation, Keyword, KeywordCategory
from twep.util import tweetanalyzer


# scans through MyTweets by screen_username and formats data
# intention is to use as cronjob in conjunction with getting new tweets, see the command get.py
# TODO: make sure no race conditions??

class Command(BaseCommand):

    help = 'Print stuff by username to a log file using > or >> in terminal'

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)

    # holy fucking loops batman wtf
    # this cannot be healthy
    def handle(self, *args, **options):
        # get the twitter user name
        sn = options['screen_name']
        ta = tweetanalyzer.TweetAnalyzer(screen_name=sn)
        situations = Situation.objects.filter(screen_name=sn)
        for sit in situations:
            print("\n")
            print("===" + sit.base_tweet.twitter_msg_id + "===")
            print(sit.base_tweet.text.encode("UTF-8"))
            if sit.children is not None:
                for sc in sit.children.all():
                    print(sc.text.encode("UTF-8"))
            print("==/" + sit.base_tweet.twitter_msg_id + "===")
            print("\n")



