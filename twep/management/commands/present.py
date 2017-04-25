from django.core.management.base import BaseCommand
from twep.models import MyTweet, Situation, Keyword


# scans through MyTweets by screen_username and formats data
# intention is to use as cronjob in conjunction with getting new tweets, see the command get_tweets.py
# TODO: make sure no race conditions??

class Command(BaseCommand):

    help = 'Print stuff by username to a log file using > or >> in terminal'

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)

    def handle(self, *args, **options):
        sn = options['screen_name']
        sits = Situation.objects.filter(base_tweet__screen_name=sn)
        for sit in sits:
            bt = sit.base_tweet
            tweets = bt.get_all_children(include_self=False)
            print("\n")
            print("====" + bt.twitter_msg_id + "====")
            print("First text:")
            print(bt.text.encode("UTF-8"))
            if bt.keyword.all().count() > 0:
                print("With keywords:")
                for kw in bt.keyword.all():
                    print(kw.word.encode("UTF-8"))
            print("With children:")
            for t in tweets:
                print(t.text.encode("UTF-8"))
                if t.keyword.all().count() > 0:
                    print("child keywords:")
                    for ckw in t.keyword.all():
                        print(ckw.word.encode("UTF-8"))
        print("\n")

