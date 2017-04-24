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
    # ASCII dog for fun
    dog = twep.settings.DOG

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)

    def handle(self, *args, **options):
        randy = randint(0, 5)
        if randy == 3:
            print(self.dog)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(now)
        sn = options['screen_name']
        t = TweetSeeker(sn)
        s = MyTweet.objects.filter(screen_name=sn).order_by('twitter_msg_id')
        try:
            latest_stored = s.reverse()[0]
        except IndexError:
            # should be in a multiple of 200, which is what the api gets per request. This can be changed with MATH!!
            at = t.download_many_tweets(limit=200)

            # log:
            print("No entries in DB for " + sn)
            num_tweets = len(at)
            print("Will attempt to make %s models." % num_tweets)
            print("Could take a while or forever. Maybe not download all tweets..")

            # store the tweets
            t.make_model(at)

            # log:
            print("Done. Try MyTweet.objects.filter(screen_name='" + sn + "')")
            return
        if latest_stored is not None:
            # fetch the latest tweet by the username from internet
            n = t.get_newest_single()
            # does its id match our latest stored twitter message id?
            if n.id_str == latest_stored.twitter_msg_id:
                print("DB up to date (only checking latest entry) for " + sn)
                return
            else:
                # the ids do not match, meaning we know that we are at least 1 tweet behind
                print(n.id_str + " != " + latest_stored.twitter_msg_id)
                print("DB not up to date for " + sn)
                # get the two hundred newest
                newest_tweets = t.get_newest_num()
                i = 0
                # compare stored ids to downloaded ids. how far back (i) do we have to go find the id?
                for nt in newest_tweets:
                    if nt.id_str == latest_stored.twitter_msg_id:
                        print("DB is %s tweets behind" % i)
                        break
                    else:
                        i += 1
                # download i tweets. Max is 200.
                # Could iterate in chunks of 200 but the database insert/transaction is REALLY. REALLY slow.
                # are tweets that old interesting? could be losing connection
                # TODO: Update from sqlite to other db driver or w/e?
                # so keep at 200 for now
                if i > 200:
                    print("More than two hundred behind. Get just 200 newest for now *cough, cough*.")
                    i = 200
                m = t.make_model(t.get_newest_num(i))

                # logging:
                print("%s created" % len(m))
        else:
            print("whats down here eh")
            return
