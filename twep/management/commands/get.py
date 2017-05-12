import datetime

from django.core.management.base import BaseCommand
from twep.util.tweets.tweettransformer import TweetTransformer
from twep.models import Tweet
from twep.util.tweets.tweetseeker import TweetSeeker


class Command(BaseCommand):

    help = 'Checks for new tweets by user and updates data'
    # limit inital get to this number
    get_no_more_than = 333
    verbose = False

    def add_arguments(self, parser):
        # pass a twitter screen name to mark the tweets with
        parser.add_argument('screen_name', type=str)
        # add the verbose flag if you
        parser.add_argument('--v', dest='verbose', action='store_true')

    def handle(self, *args, **options):
        sn = options['screen_name']
        if options['verbose']:
            self.verbose = True
        vprint = print if self.verbose else lambda *a, **k: None
        vprint(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        seeker = TweetSeeker(screen_name=sn, verbose=self.verbose)
        trans = TweetTransformer(screen_name=sn, verbose=self.verbose)
        try:
            # get tweet with latest created date
            latest_stored = Tweet.objects.filter(screen_name=sn).latest('created_at')
            # latest_stored = tweets.latest('created_at')
            vprint("Latest stored is " + latest_stored.twitter_msg_id)
            n = seeker.get_newest_single()
            # does its id match our latest stored twitter message id?
            if n.id_str == latest_stored.twitter_msg_id:
                # print both ids to assure the user that they are the same
                vprint(n.id_str + "=" + latest_stored.twitter_msg_id)
                print("DB up to date")
                return
            else:
                # the ids do not match, meaning we know that we are at least 1 tweet behind
                vprint("Updating " + sn)

                # how far behind is the db?
                difference = seeker.get_num_new_since_id(latest_stored.twitter_msg_id)

                # list of created tweets
                created = trans.make_model(difference)

                print("%s created" % len(created))
                return
        except Tweet.DoesNotExist:
            vprint("No entries in DB for " + sn)
            vprint("Download %s " % self.get_no_more_than + "tweets")
            # should be in a multiple of 200, which is what the api gets per request. This can be changed with MATH!!
            at = seeker.get_num_newest_tweets(limit=self.get_no_more_than)
            vprint("Make %s models" % len(at))
            start = datetime.datetime.now()
            # store the tweets and time it
            models = trans.make_model(at)
            end = datetime.datetime.now()
            # calculate the time it took to make the entries
            vprint(end - start)
            print("%s created" % len(models))
            return

