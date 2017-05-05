import datetime

from django.core.management.base import BaseCommand

from twep.util.text import markdown
from twep.util.tweets.tweettransformer import TweetTransformer

import twep.settings
from twep.models import MyTweet
from twep.util.tweets.tweetseeker import TweetSeeker


class Command(BaseCommand):

    help = 'Checks for new tweets by user and updates data'
    get_no_more_than = 1000
    colors = twep.settings.COLORS
    verbose = False

    def vprint(self, text):
        if self.verbose:
            print(text)

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)
        parser.add_argument('--v', dest='verbose', action='store_true')

    def handle(self, *args, **options):
        mark = markdown.MarkDown()
        m = mark.header_1("Here is a table")\
            .Table().header("Category").header("Keyword").header("Mambo")\
            .entry("Danger", ["Knivstukket", "no. 5"])\
            .entry("Resolved", ["I arrest", "no. 6"]).make()\
            .text("and some text under it")\
            .header_1("Here is some python code:")\
            .Code("python")\
            .add_line("if foo:").add_line("print('foo!')", 1)\
            .add_line("else:").add_line("print('bar')", 1)\
            .make()\
            .Code("javascript")\
            .add_line("console.log('foo');").make()\
            .text("Bye bye")
        print(m)

        exit()


        if options['verbose']:
            self.verbose = True
        vprint = print if self.verbose else lambda *a, **k: None
        vprint(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        sn = options['screen_name']
        seeker = TweetSeeker(screen_name=sn)
        trans = TweetTransformer(screen_name=sn)
        try:
            # get tweet with latest created date
            latest_stored = MyTweet.objects.filter(screen_name=sn).latest('created_at')
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
            end = datetime.datetime.now()
            vprint(end - start)
            print("%s created" % len(models))
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
                vprint(n.id_str + " != " + latest_stored.twitter_msg_id)
                vprint("DB not up to date for " + sn)

                # how far behind is the db?
                num_behind = seeker.get_num_new_since_id(latest_stored.twitter_msg_id)
                # don't want too many tweets
                if num_behind > self.get_no_more_than:
                    vprint("Very far behind. Get just %s newest for now *cough, cough*." % self.get_no_more_than)
                    num_behind = self.get_no_more_than
                created = trans.make_model(seeker.get_newest_num(num_behind))

                # logging:
                print("%s created" % len(created))
                return

