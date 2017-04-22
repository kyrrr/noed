from django.core.management.base import BaseCommand, CommandError
from twep.tweepyImpl import TweetSeeker
from twep.models import MyTweet
import datetime
from twep import logger
from subprocess import call
import sys, select


class Command(BaseCommand):

    help = 'Checks for new tweets by user and updates data'
    # hold log message
    msg = "\n"

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)

    def handle(self, *args, **options):
        now = datetime.datetime.now().strftime('%Y-%m-%d:%H-%M-%S')
        self.msg = self.msg + now + "\n"
        sn = options['screen_name']
        log = logger.Logger(sn)
        t = TweetSeeker(sn)
        s = MyTweet.objects.filter(screen_name=sn).order_by('twitter_msg_id')
        try:
            latest_stored = s.reverse()[0]
        except IndexError:
            self.msg = self.msg + "No entries in DB for " + sn + "\n"
            log.log(self.msg)
            # LOL
            # call(["/Library/Frameworks/Python.framework/Versions/3.6/bin/python3", "manage.py", "downloadall", sn])
            return
        if latest_stored is not None:
            # fetch the latest tweet by the username from internet
            n = t.get_newest_single()
            # does its id match our latest stored twitter message id?
            if n.id_str == latest_stored.twitter_msg_id:
                self.msg = self.msg + "DB up to date (only checking latest entries) " + sn + "\n"
                # self.msg = self.msg + " " + n.id_str + " == " + l.twitter_msg_id + "\n"
                log.log(self.msg)
            else:
                # it does not
                self.msg = self.msg + n.id_str + " != " + latest_stored.twitter_msg_id + "\n"
                # get the two hundred newest
                gnc = t.get_newest_count()
                print(type(gnc))
                i = 0
                for nc in gnc:
                    if nc.id_str == latest_stored.twitter_msg_id:
                        self.msg = self.msg + "Match after %s tweets" % i + "\n"
                    else:
                        i += 1
                cn = t.get_newest_count(i)
                j = 0
                # loop through newest i tweets
                for n in cn:
                    # if the id exists
                    exists = MyTweet.objects.filter(twitter_msg_id=n.id_str)
                    if len(exists) > 0:
                        # exit the loop
                        continue
                    else:
                        # create new models
                        MyTweet.objects.get_or_create(
                            twitter_msg_id=n.id_str,
                            screen_name=sn,
                            text=n.text.encode("utf-8"),
                            reply_to=n.in_reply_to_status_id_str,
                            created_at=n.created_at,
                        )
                        self.msg = self.msg + n.id_str + "\n"
                        j += 1
                self.msg = self.msg + " created %s " % j + " models" + "\n"
                log.log(self.msg)
        else:
            log.log(self.msg)
            return
