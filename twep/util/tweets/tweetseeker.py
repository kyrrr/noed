import tweepy
from twep import settings
from twep.models import MyTweet

# An implementation of necessary tweepy functionality
# Or is it?? It's just what I need is what it is
# Is based on a user and their tweets.
# Uses keys from settings.py when initialized
# Gets tweets in a lot of ways
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
        # print("Authenticated")
        self.screen_name = screen_name

    # Put your twitter api keys in settings.py
    def authenticate(self):
        keys = settings.API_KEYS['TWITTER']
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

    def get_num_new_since_id(self, latest_stored_id, look_back=200):
        # 200!!! never forget it's just 200 at a time
        newest_tweets = self.get_num_newest_tweets(look_back)
        # compare stored ids to downloaded ids. how far back (i) do we have to go find the id?
        for i, nt in enumerate(newest_tweets):
            if nt.id_str == latest_stored_id:
                return i

    # download tweets from user up to a limit. Higher limit means slow DB insert later on..
    # TODO: is sqlite bad?
    def get_num_newest_tweets(self, limit):
        all_tweets = []  # store tweets
        newest_tweets = self.get_newest_num(self.screen_name)  # fetch 200 newest
        all_tweets.extend(newest_tweets)  # add newest
        oldest = all_tweets[-1].id - 1  # what
        while len(newest_tweets) > 0:
            newest_tweets = self.get_tweets_under_id(oldest)
            all_tweets.extend(newest_tweets)
            oldest = all_tweets[-1].id - 1
            if len(all_tweets) > limit:
                trimmed_tweets = all_tweets[:limit]
                return trimmed_tweets
        return all_tweets  # i dont think this will kick in when there is a limit with a default BUT IT DO

