import tweepy
from twep import settings
from twep.models import MyTweet


# An implementation of necessary tweepy functionality
# Can transform tweepy tweets to modeled objects
class Tweets:

    # holds an OAuth object
    auth = None
    # holds the tweepy api
    api = None
    # use to hold downloaded tweepy objects
    all_tweets = []
    # hold our tweet models
    modeled_tweets = []
    # screen name
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

    def get_newest_single(self):
        newest = self.api.user_timeline(screen_name=self.screen_name, count=1)
        for new in newest:
            return new

    def get_newest_count(self, count=200):
        return self.api.user_timeline(screen_name=self.screen_name, count=count)

    def get_tweets_under_id(self, max_id):
        return self.api.user_timeline(screen_name=self.screen_name, max_id=max_id, count=200)

    def get_tweet(self, tweet_id):
        return self.api.statuses_lookup(tweet_id)

    def download_all_tweets(self):
        all_tweets = []  # store tweets
        print("Get newest...")
        newest_tweets = self.get_newest_count(self.screen_name)  # fetch 200 newest
        all_tweets.extend(newest_tweets)  # add newest
        print(len(all_tweets))
        oldest = all_tweets[-1].id - 1  # what
        while len(newest_tweets) > 0:
            print("Getting up to id %s" % oldest)
            newest_tweets = self.get_tweets_under_id(oldest)
            all_tweets.extend(newest_tweets)
            print(len(all_tweets))
            oldest = all_tweets[-1].id - 1

        self.all_tweets = all_tweets

    def make_model(self, tweets):
        # print("Make model of num tweets %s" % len(tweets))
        modeled_tweets = []
        for t in tweets:
            m = MyTweet.objects.create(
                twitter_msg_id=t.id_str,
                screen_name=self.screen_name,
                text=t.text.encode("utf-8"),
                reply_to=t.in_reply_to_status_id_str,
                created_at=t.created_at,
            )
            modeled_tweets.append(m)
        return modeled_tweets

    def count_num_new(self, cur_newest_id):
        nt = self.get_newest_count()
        i = 0
        for t in nt:
            if t.id_str is cur_newest_id:
                return i
            else:
                i += 1
        return i
