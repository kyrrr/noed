from django.core.management.base import BaseCommand, CommandError
from twep.tweepyImpl import TweetSeeker
from twep.models import MyTweet
import datetime
from twep import logger
import sys, select


class Command(BaseCommand):

    help = 'Download all tweets by user'
    # hold log message
    msg = "\n"

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)

    def handle(self, *args, **options):
        sn = options['screen_name']
        log = logger.Logger(sn)
        t = TweetSeeker(sn)
        at = t.download_all_tweets()
        ms = t.make_model(at)
        self.msg = self.msg + " %s new models " % len(ms)
        for m in ms:
            m.save()
        log.log(self.msg)
