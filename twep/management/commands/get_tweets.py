import datetime
from django.core.management.base import BaseCommand
from twep.models import MyTweet
from twep.util.tweetseeker import TweetSeeker
from twep.util.tweettransformer import TweetTransformer


class Command(BaseCommand):

    help = 'Checks for new tweets by user and updates data'

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)

    def handle(self, *args, **options):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(now)
        sn = options['screen_name']
        t = TweetSeeker(screen_name=sn)
        tr = TweetTransformer(screen_name=sn)
        s = MyTweet.objects.filter(screen_name=sn).order_by('twitter_msg_id')
        try:
            latest_stored = s.reverse()[0]
        except IndexError:
            # log:
            print("No entries in DB for " + sn)
            print("Will download tweets")
            # should be in a multiple of 200, which is what the api gets per request. This can be changed with MATH!!
            at = t.get_num_newest_tweets(limit=200)
            print("Will attempt to make %s models." % len(at))
            print("Could take a while or forever.")
            start = datetime.datetime.now()
            # store the tweets
            tr.make_model(at)
            end = datetime.datetime.now()
            print("Done in %s somethings" % (end - start))
            # log:
            print("Try MyTweet.objects.filter(screen_name='" + sn + "')")
            return
        if latest_stored is not None:
            # fetch the latest tweet by the username from internet
            n = t.get_newest_single()
            # does its id match our latest stored twitter message id?
            if n.id_str == latest_stored.twitter_msg_id:
                print("DB up to date (only checking latest entry) for " + sn)
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
                created = tr.make_model(t.get_newest_num(i))

                # logging:
                print("%s created" % len(created))
        else:
            print("whats down here eh")
            return
