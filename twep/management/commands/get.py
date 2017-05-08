import datetime

from django.core.management.base import BaseCommand

from twep.util.text import markdown
from twep.util.tweets.tweettransformer import TweetTransformer

import twep.settings
from twep.models import Tweet
from twep.util.tweets.tweetseeker import TweetSeeker


class Command(BaseCommand):

    help = 'Checks for new tweets by user and updates data'
    get_no_more_than = 1000
    colors = twep.settings.COLORS
    verbose = False

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)
        parser.add_argument('--v', dest='verbose', action='store_true')

    def handle(self, *args, **options):
        # Tweet.objects.all().delete()  # TODO: REMOVE AFTER DEBUG
        if options['verbose']:
            self.verbose = True
        vprint = print if self.verbose else lambda *a, **k: None
        vprint(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        sn = options['screen_name']
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
                vprint(n.id_str + "=" + latest_stored.twitter_msg_id)
                print("DB up to date")
                return
            else:
                # the ids do not match, meaning we know that we are at least 1 tweet behind
                vprint("Updating " + sn)

                # how far behind is the db?
                difference = seeker.get_num_new_since_id(latest_stored.twitter_msg_id)
                # don't want too many tweets
                # if len(difference) > self.get_no_more_than:
                # vprint("Very far behind. Get just %s newest for now *cough, cough*." % self.get_no_more_than)
                # difference = self.get_no_more_than
                created = trans.make_model(difference)

                # logging:
                print("%s created" % len(created))
                # vprint("Total %s " % tweets.count())
                return
            # vprint("Total %s " % tweets.count())
            # exit("phew")
        except Tweet.DoesNotExist:
            # log:
            # exit("once")
            vprint("No entries in DB for " + sn)
            vprint("Download %s " % self.get_no_more_than + "tweets")
            # should be in a multiple of 200, which is what the api gets per request. This can be changed with MATH!!
            at = seeker.get_num_newest_tweets(limit=self.get_no_more_than)
            vprint("Make %s models" % len(at))
            start = datetime.datetime.now()
            # store the tweets and time it
            models = trans.make_model(at)
            end = datetime.datetime.now()
            vprint(end - start)
            print("%s created" % len(models))
            return

