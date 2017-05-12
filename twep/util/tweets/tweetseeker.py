import tweepy
from twep import settings
from twep.models import Tweet

# An implementation of necessary tweepy functionality
# Or is it?? It's just what I need is what it is
# Is based on a user and their tweets.
# Uses keys from settings.py when initialized
# Gets tweets in a lot of ways
# Needs a twitter screen name (url name) when initialized


class TweetSeeker:

    # when this class is constructed, authenticate using settings.py
    def __init__(self, screen_name, verbose=False):
        self.api = tweepy.API(self.authenticate())
        # print("Authenticated")
        self.screen_name = screen_name
        self.vprint = print if verbose else lambda *a, **k: None

    # Put your twitter api keys in settings.py
    def authenticate(self):
        keys = settings.API_KEYS['TWITTER']
        auth = tweepy.OAuthHandler(keys['CONSUMER_KEY'], keys['CONSUMER_SECRET'])
        auth.set_access_token(keys['ACCESS_TOKEN'], keys['ACCESS_SECRET'])
        return auth

    # get a single id'ed? ided? tweet from user by id. id is the thing here, and just one tweet.
    def get_tweet(self, tweet_id):
        self.vprint("Get tweet " + tweet_id)
        return self.api.statuses_lookup(tweet_id)

    def get_newest_single(self):
        self.vprint("Get newest tweet")
        newest = self.api.user_timeline(screen_name=self.screen_name, count=1)
        for new in newest:
            return new

    def simple_get_newest_num(self, count=200):
        self.vprint("Get newest %s tweets" % count)
        return self.api.user_timeline(screen_name=self.screen_name, count=count)

    # get tweets, but stop under max_id
    def get_tweets_under_id(self, max_id):
        self.vprint("Get under id %s" % max_id)
        return self.api.user_timeline(screen_name=self.screen_name, max_id=max_id, count=200)

    def get_num_new_since_id(self, latest_stored_id, look_back=256):
        self.vprint("Get %s " % look_back + "tweets since " + latest_stored_id)
        newest_tweets = self.get_num_newest_tweets(look_back)
        # compare stored ids to downloaded ids. how far back (i) do we have to go find the id?
        for i, nt in enumerate(newest_tweets):
            if nt.id_str == latest_stored_id:
                return self.get_num_newest_tweets(i)

    # download tweets from user up to a limit. Higher limit means slow DB insert later on..
    # TODO: is sqlite bad?
    def get_num_newest_tweets(self, limit):
        all_tweets = []  # store tweets
        newest_tweets = self.simple_get_newest_num()  # fetch 200 newest
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

