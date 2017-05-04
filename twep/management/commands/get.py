import datetime

from django.core.management.base import BaseCommand
from twep.util.tweettransformer import TweetTransformer

import twep.settings
from twep.models import MyTweet
from twep.util.tweets.tweetseeker import TweetSeeker


class Command(BaseCommand):

    help = 'Checks for new tweets by user and updates data'
    get_no_more_than = 1000
    colors = twep.settings.COLORS

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)

    def handle(self, *args, **options):
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        sn = options['screen_name']
        seeker = TweetSeeker(screen_name=sn)
        trans = TweetTransformer(screen_name=sn)
        try:
            # get tweet with latest created date
            latest_stored = MyTweet.objects.filter(screen_name=sn).latest('created_at')
        except MyTweet.DoesNotExist:
            # log:
            print("No entries in DB for " + sn)
            print("Will download tweets")
            # should be in a multiple of 200, which is what the api gets per request. This can be changed with MATH!!
            at = seeker.get_num_newest_tweets(limit=self.get_no_more_than)
            print("Will attempt to make %s models." % len(at))
            print("Could take a while or forever.")
            start = datetime.datetime.now()
            # store the tweets and time it
            trans.make_model(at)
            end = datetime.datetime.now()
            print(end - start)
            # log:
            print("Try MyTweet.objects.filter(screen_name='" + sn + "')")
            return
        if latest_stored is not None:
            # fetch the latest tweet by the username from internet
            n = seeker.get_newest_single()
            # does its id match our latest stored twitter message id?
            if n.id_str == latest_stored.twitter_msg_id:
                print(self.colors['GREEN'] + n.id_str + "=" + latest_stored.twitter_msg_id + self.colors['END'])
                print(self.colors['BLUE'] + "DB up to date (only checking latest entry) for " + sn + self.colors['END'])
                return
            else:
                # the ids do not match, meaning we know that we are at least 1 tweet behind
                print(n.id_str + " != " + latest_stored.twitter_msg_id)
                print("DB not up to date for " + sn)

                # how far behind is the db?
                num_behind = seeker.get_num_new_since_id(latest_stored.twitter_msg_id)
                # don't want too many tweets
                if num_behind > self.get_no_more_than:
                    print("Very far behind. Get just %s newest for now *cough, cough*." % self.get_no_more_than)
                    num_behind = self.get_no_more_than
                created = trans.make_model(seeker.get_newest_num(num_behind))

                # logging:
                print("%s created" % len(created))
                print('try "python manage.py scan ' + sn + '"')
                return

