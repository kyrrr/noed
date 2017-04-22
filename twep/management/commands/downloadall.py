from django.core.management.base import BaseCommand

from twep.util import logger
from twep.util.tweetseeker import TweetSeeker


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
