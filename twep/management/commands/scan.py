from django.core.management.base import BaseCommand
from twep.models import MyTweet, Situation, Keyword
from twep.util import tweettransformer


# scans through MyTweets by screen_username and formats data
# intention is to use as cronjob in conjunction with getting new tweets, see the command get_tweets.py
# TODO: make sure no race conditions??

class Command(BaseCommand):

    help = 'Scans tweet text for EMERGENCIES!!!'
    # hold log message
    msg = "\n"

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)

    def handle(self, *args, **options):
        sn = options['screen_name']
        tr = tweettransformer.TweetTransformer(sn)
        tr.set_parent_child()
        tr.make_timeline()
        tr.scan('Danger')  # TODO: consts?
        tr.scan('Status')
        tr.scan('Location')
        tr.scan('Actor')

        # TODO: this elsewhere. Here for convenience
        many_cats = MyTweet.objects.filter(parent__isnull=True)

        for cat in many_cats:
            try:
                sit = Situation.objects.get(base_tweet=cat)
            except Situation.DoesNotExist:
                # print("Situation for base tweet does not exist")
                continue
            kw = cat.keyword.all()
            print(cat.twitter_msg_id)
            children = sit.base_tweet.get_all_children(include_self=False)
            print("has %s child(ren) " % len(children))
            for c in children:
                print(c.twitter_msg_id)
                print(c.text.encode("UTF-8"))
                print("child keywords:")
                for f in c.keyword.all():
                    print(f.category)
                    print(f.word.encode("UTF-8"))
            print("found keywords:")
            for k in kw:
                print(k.category + ":")
                print(k.word.encode("UTF-8"))
            print("in text:")
            print(cat.text.encode("UTF-8"))
            print("=============")
