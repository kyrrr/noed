from django.core.management.base import BaseCommand, CommandError
from twep.tweepyImpl import Tweets
from twep.models import MyTweet
import datetime
from twep import logger
import sys, select


class Command(BaseCommand):

    help = 'Checks for new tweets by user and updates data'
    # hold log message
    msg = ''

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)

    def handle(self, *args, **options):
        now = datetime.datetime.now().strftime('%Y-%m-%d:%H-%M-%S')
        self.msg = self.msg + now
        sn = options['screen_name']
        log = logger.Logger(sn)
        t = Tweets(sn)
        s = MyTweet.objects.filter(screen_name=sn).order_by('twitter_msg_id')
        try:
            l = s.reverse()[0]
        except IndexError:
            self.msg = self.msg + "\n" + ": No entries in DB for " + sn + "\n"
            log.log(self.msg)
            return
        if l is not None:
            n = t.get_newest_single()
            if n.id_str == l.twitter_msg_id:
                self.msg = self.msg + "\n" + ": DB up to date (only checking first latest entries) " + sn + "\n"
                self.msg = self.msg + "\n" + " " + n.id_str + " == " + l.twitter_msg_id + "\n"
                log.log(self.msg)
            else:
                self.msg = self.msg + "\n" + n.id_str + " != " + l.twitter_msg_id + "\n"
                gnc = t.get_newest_count()
                i = 0
                for nc in gnc:
                    if nc.id_str == l.twitter_msg_id:
                        self.msg = self.msg + "Match after %s tweets" % i + "\n"
                    else:
                        i += 1
                cn = t.get_newest_count(i)
                j = 0
                for n in cn:
                    MyTweet.objects.get_or_create(
                        twitter_msg_id=n.id_str,
                        screen_name=sn,
                        text=n.text.encode("utf-8"),
                        reply_to=n.in_reply_to_status_id_str,
                        created_at=n.created_at,
                    )
                    self.msg = self.msg + n.id_str + "\n"
                    j += 1
                self.msg = self.msg + " created or updated %s " % j + " models" + "\n"
                log.log(self.msg)
        else:
            log.log(self.msg)
            return
