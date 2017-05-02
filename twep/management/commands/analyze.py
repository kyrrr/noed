from django.core.management.base import BaseCommand
from twep.models import MyTweet, Situation, Keyword, KeywordCategory, Location
from twep.util import tweetanalyzer


# scans through MyTweets by screen_username and formats data
# intention is to use as cronjob in conjunction with getting new tweets, see the command get.py
# TODO: make sure no race conditions??

class Command(BaseCommand):

    help = 'Print stuff by username to a log file using > or >> in terminal'

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)

    # holy fucking loops batman wtf
    # this cannot be healthy
    def handle(self, *args, **options):
        # get the twitter user name
        sn = options['screen_name']
        situations = Situation.objects.filter(screen_name=sn)
        for sit in situations:
            print("===" + sit.base_tweet.twitter_msg_id + "===")
            print("First text:")
            print(sit.base_tweet.text.encode("UTF-8"))
            try:
                l = Location.objects.get(mytweet=sit.base_tweet)
                print("Possible location:")
                print(l.sub_district.name.encode("UTF-8"))
            except Location.DoesNotExist:
                pass
            if sit.children.all().count() > 0:
                print("Children texts:")
                for sc in sit.children.all():
                    print(sc.text.encode("UTF-8"))
                    try:
                        cl = Location.objects.get(mytweet=sit.base_tweet)
                        print("Possible location:")
                        print(cl.sub_district.name.encode("UTF-8"))
                    except Location.DoesNotExist:
                        pass
                    if sc.get_last_parent() and sit.base_tweet == sc.get_last_parent():
                        pass
                        # print(sc.get_last_parent().text.encode("UTF-8"))
                        # print("SAME")
            print("==/" + sit.base_tweet.twitter_msg_id + "===")
            print("\n")



