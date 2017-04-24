import tweepy
from twep import settings
from twep.models import MyTweet


# An implementation of necessary tweepy functionality
# Or is it?? It's just what I need is what it is
# Is based on a user and their tweets.
# Needs a twitter screen name (url name) when initialized
class TweetSeeker:

    # holds an OAuth object
    auth = None
    # holds the tweepy api
    api = None
    # screen name.
    screen_name = None

    # when this class is constructed, authenticate using settings.py
    def __init__(self, screen_name):
        self.authenticate()
        self.api = tweepy.API(self.auth)
        self.screen_name = screen_name

    # Put your twitter api keys in settings.py
    def authenticate(self):
        keys = settings.API_KEYS[0]['TWITTER']
        auth = tweepy.OAuthHandler(keys['CONSUMER_KEY'], keys['CONSUMER_SECRET'])
        auth.set_access_token(keys['ACCESS_TOKEN'], keys['ACCESS_SECRET'])
        self.auth = auth

    # get a single id'ed? ided? tweet from user by id. id is the thing here, and just one tweet.
    def get_tweet(self, tweet_id):
        return self.api.statuses_lookup(tweet_id)

    def get_newest_single(self):
        newest = self.api.user_timeline(screen_name=self.screen_name, count=1)
        for new in newest:
            return new

    def get_newest_num(self, count=200):
        return self.api.user_timeline(screen_name=self.screen_name, count=count)

    # get tweets, but stop under max_id
    def get_tweets_under_id(self, max_id):
        return self.api.user_timeline(screen_name=self.screen_name, max_id=max_id, count=200)

    # download tweets from user up to a limit. Higher limit means slow DB insert later on..
    def download_many_tweets(self, limit=1000):
        all_tweets = []  # store tweets
        print("Get many tweets, limit to %s" % limit)
        print("Get newest...")
        newest_tweets = self.get_newest_num(self.screen_name)  # fetch 200 newest
        all_tweets.extend(newest_tweets)  # add newest
        print(len(all_tweets))
        oldest = all_tweets[-1].id - 1  # what
        while len(newest_tweets) > 0:
            print("Getting up to id %s" % oldest)
            newest_tweets = self.get_tweets_under_id(oldest)
            all_tweets.extend(newest_tweets)
            print(len(all_tweets))
            oldest = all_tweets[-1].id - 1
            if len(all_tweets) > limit:
                trimmed_tweets = all_tweets[:limit]
                return trimmed_tweets

        return all_tweets

    # makes models of tweets. if the tweet is a reply, first make a model of that tweet.
    # TODO: reply_to as actual foreign key to another MyTweet object. Just a string for now.
    def make_model(self, tweets):
        gotten_or_created = []
        for t in tweets:
            exists = MyTweet.objects.filter(twitter_msg_id=t.id_str)
            if len(exists) > 0:
                # exit the loop
                continue
            if t.in_reply_to_status_id_str:
                self.make_model(self.get_tweet(t.in_reply_to_status_id_str))
            gotten_or_created.append(
                MyTweet.objects.get_or_create(
                    # this is used as the db primary key
                    twitter_msg_id=t.id_str,
                    screen_name=self.screen_name,
                    text=t.text.encode("UTF-8"),
                    # used to assign an object self-reference in models.
                    reply_to_id_str=t.in_reply_to_status_id_str,
                    created_at=t.created_at,
                )
            )
        return gotten_or_created
