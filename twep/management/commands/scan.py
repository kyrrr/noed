from django.core.management.base import BaseCommand
from twep.models import MyTweet, Situation
from twep.util import logger
from twep.util import scraper


# scans through MyTweets by screen_username and formats data
# intention is to use as cronjob in conjunction with getting new tweets, see the command get_tweets.py
# TODO: make sure no race conditions??

class Command(BaseCommand):

    help = 'Scans tweet text for EMERGENCIES!!!'
    # hold log message
    msg = "\n"

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)

    def handle(self, *args, **options):
        sn = options['screen_name']
        s = scraper.Scraper(sn)
        # all = MyTweet.objects.all()
        s.set_reply_timeline()
        s.situate()
        # not_scanned = MyTweet.objects.filter(screen_name=sn).filter(scanned=False)
        # are_replies = not_scanned.filter(reply_to_id_str__isnull=False)  # .filter(reply_to_object__isnull=True)
        # for reply in are_replies:
            # try:
                # parent = MyTweet.objects.get(twitter_msg_id=reply.reply_to_id_str)
                # reply.parent = parent
                # parent.child = reply
                # print(reply.text)
                # print("is self reply to")
                # print(parent.text)
            # except MyTweet.DoesNotExist:
                # pass
                # print(reply.twitter_msg_id + " is reply but not to self")

        # last = MyTweet.objects.filter(parent__isnull=False).filter()

