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
        pass