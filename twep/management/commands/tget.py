import datetime

from django.core.management.base import BaseCommand

from twep.util.text import markdown
from twep.util.tweets.tweettransformer import TweetTransformer

import twep.settings
from twep.models import MyTweet, User
from twep.util.tweets.tweetseeker import TweetSeeker


class Command(BaseCommand):

    help = 'Checks for new tweets by user and updates data'
    get_no_more_than = 200
    verbose = False
    models = []

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)
        parser.add_argument('--v', dest='verbose', action='store_true')

    def handle(self, *args, **options):
        if options['verbose']:
            self.verbose = True
        vprint = print if self.verbose else lambda *a, **k: None
        vprint(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        sn = options['screen_name']
        user_tuple = User.objects.get_or_create(screen_name=sn)
        user = None
        for datum in user_tuple:
            if isinstance(datum, bool):
                if datum:
                    print("Create new user")
            if isinstance(datum, User):
                user = datum
        seeker = TweetSeeker(screen_name=user.screen_name)
        trans = TweetTransformer(screen_name=user.screen_name)
        try:
            # get tweet with latest created date
            latest_stored = MyTweet.objects.filter(user=user).latest('created_at')
        except MyTweet.DoesNotExist:
            # log:
            vprint("No entries in DB for " + sn)
            vprint("Will download tweets")
            # should be in a multiple of 200, which is what the api gets per request. This can be changed with MATH!!
            at = seeker.get_num_newest_tweets(limit=self.get_no_more_than)
            vprint("Will attempt to make %s models." % len(at))
            vprint("Could take a while or forever.")
            start = datetime.datetime.now()
            # store the tweets and time it
            models = trans.make_model(at)
            for id, m in models.items():
                user.mytweet_set.add(m)
            end = datetime.datetime.now()
            vprint(end - start)
            print("%s tweets created" % len(models))
            return
        if latest_stored is not None:
            # fetch the latest tweet by the username from internet
            n = seeker.get_newest_single()
            # does its id match our latest stored twitter message id?
            if n.id_str == latest_stored.twitter_msg_id:
                # print(n.id_str + "=" + latest_stored.twitter_msg_id)
                # print("DB up to date (only checking latest entry) for ")
                print("0 tweets created")
                return
            else:
                # the ids do not match, meaning we know that we are at least 1 tweet behind
                vprint(n.id_str + " != " + latest_stored.twitter_msg_id)
                vprint("DB not up to date for " + sn)

                # how far behind is the db?
                num_behind = seeker.get_num_new_since_id(latest_stored.twitter_msg_id)
                # don't want too many tweets
                if num_behind > self.get_no_more_than:
                    vprint("Very far behind. Get just %s newest for now *cough, cough*." % self.get_no_more_than)
                    num_behind = self.get_no_more_than
                created = trans.make_model(seeker.get_newest_num(num_behind))
                for id, m in created.items():
                    user.mytweet_set.add(m)
                # logging:
                print("%s tweets created" % len(created))
                return

