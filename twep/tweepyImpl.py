import tweepy
import datetime
from twep import settings
import csv
from twep.models import MyTweet


class UserTweetsThing:

    auth = None
    api = None
    tweets = []

    def __init__(self):
        self.authenticate()
        self.api = tweepy.API(self.auth)

    # Reads your keys from twep/settings.py
    def authenticate(self):
        keys = settings.API_KEYS[0]['TWITTER']
        auth = tweepy.OAuthHandler(keys['CONSUMER_KEY'], keys['CONSUMER_SECRET'])
        auth.set_access_token(keys['ACCESS_TOKEN'], keys['ACCESS_SECRET'])
        self.auth = auth

    def get_newest(self, username, count=200):
        return self.api.user_timeline(screen_name=username, count=count)

    def get_tweet(self, tweet_id):
        return self.api.statuses_lookup(tweet_id)

    def make_model(self, screen_name, tweets):
        for t in tweets:
            e = MyTweet.objects.create(
                screen_name=screen_name,
                text=t.text.encode("utf-8"),
                reply_to=t.in_reply_to_status_id_str,
                situation_status="idfk",
                twitter_msg_id=t.id_str,
                created_at=t.created_at
            )
            e.save()







