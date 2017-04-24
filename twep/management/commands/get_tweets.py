import datetime
from django.core.management.base import BaseCommand
from twep.models import MyTweet
from twep.util import logger
from twep.util.tweetseeker import TweetSeeker
import twep.settings
from random import randint
from subprocess import call


class Command(BaseCommand):

    help = 'Checks for new tweets by user and updates data'
    # hold log message
    msg = "\n"

    dog = twep.settings.DOG

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)

    def handle(self, *args, **options):
        randy = randint(0, 1)
        if randy == 1:
            self.msg += self.dog + "\n"
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.msg += now + "\n"
        sn = options['screen_name']
        log = logger.Logger(sn)
        t = TweetSeeker(sn)
        s = MyTweet.objects.filter(screen_name=sn).order_by('twitter_msg_id')
        try:
            latest_stored = s.reverse()[0]
        except IndexError:
            # LOL
            # call(["/Library/Frameworks/Python.framework/Versions/3.6/bin/python3", "manage.py", "downloadall", sn])

            # should be in a multiple of 200, which is what the api gets per request. This can be changed with MATH!!
            at = t.download_many_tweets(limit=200)

            # log:
            self.msg += "No entries in DB for " + sn + "\n"
            num_tweets = len(at)
            self.msg += "Will attempt to make %s models." % num_tweets + "\n" \
                        "Could take a while or forever. Maybe not download all tweets.." + "\n"

            # store the tweets
            t.make_model(at)

            # log:
            self.msg += "Done. Try MyTweet.objects.filter(screen_name='" + sn + "')" + "\n"
            log.log(self.msg)
            return
        if latest_stored is not None:
            # fetch the latest tweet by the username from internet
            n = t.get_newest_single()
            # does its id match our latest stored twitter message id?
            if n.id_str == latest_stored.twitter_msg_id:
                self.msg = self.msg + "DB up to date (only checking latest entry) " + sn + "\n"
                # self.msg = self.msg + " " + n.id_str + " == " + l.twitter_msg_id + "\n"
                log.log(self.msg)
                return
            else:
                # the ids do not match, meaning we know that we are at least 1 tweet behind
                self.msg = self.msg + n.id_str + " != " + latest_stored.twitter_msg_id + "\n"
                # get the two hundred newest
                newest_tweets = t.get_newest_num()
                i = 0
                # compare stored ids to downloaded ids. how far back (i) do we have to go find the id?
                for nt in newest_tweets:
                    if nt.id_str == latest_stored.twitter_msg_id:
                        self.msg += "Match after %s tweets" % i + "\n"
                    else:
                        i += 1
                # download i tweets. Max is 200.
                # Could iterate in chunks of 200 but the database insert/transaction is REALLY. REALLY slow.
                # TODO: Update from sqlite to other db driver or w/e?
                # so keep at 200 for now
                if i > 200:
                    self.msg += "More than two hundred behind. Get just 200 newest for now *cough, cough*." + "\n"
                    i = 200
                cn = t.get_newest_num(i)
                m = t.make_model(cn)

                # logging:
                self.msg += "%s created" % len(m) + "\n"
                log.log(self.msg)

        else:
            log.log(self.msg)
            return
