import time
import re
from twep.models import MyTweet, Keyword, KeywordCategory, Situation, Location


class TweetTransformer:

    screen_name = None

    # TODO: use booleans to guarantee an order to things? Meh

    def __init__(self, screen_name):
        self.screen_name = screen_name

    def get_latest(self):
        return MyTweet.objects.filter(screen_name=self.screen_name).latest('created_at')

    # places tweets in a "situation" object, in the order they were tweeted
    # also picks up single tweets which is not a bad idea
    def make_situation(self):
        user_tweets = MyTweet.objects.filter(screen_name=self.screen_name)  # TODO: filter scanned false
        # print("%s" % user_tweets.count() + " to be put in Situations " + self.screen_name)
        created = {}
        for ut in user_tweets:
            # is the tweet either a parent without a parent, or a "lonely" object
            # it can form the base of a "situation"
            # if MyTweet.is_orphan_with_child(ut) or MyTweet.is_alone(ut):
            if MyTweet.is_first_in_series(ut):
                s = Situation.objects.get_or_create(
                    screen_name=ut.screen_name,
                    first_tweet=ut
                )
                # s[1] is a boolean, true if created - false if gotten. I don't care about those,
                # just make sure all situations are updated
                s_obj = s[0]
                for c in MyTweet.get_all_children(ut, include_self=False):
                    s_obj.children.add(c)
                created[s_obj.id] = s_obj
        # we have to ensure the newest tweets also get in, so just scan everything...
        # probably we will not have 1000 tweets to care about "in production"
        # print("Found or created %s" % len(created) + " new situations for " + self.screen_name)
        return created

    # assigns parent and child to tweets
    def set_child_parent(self):
        tweets = MyTweet.objects.filter(screen_name=self.screen_name)  # TODO: filter scanned false
        are_replies = tweets.filter(reply_to_id_str__isnull=False)
        i = 0
        for i, child in enumerate(are_replies):
            try:
                # find the tweet that was replied to
                parent = MyTweet.objects.get(twitter_msg_id=child.reply_to_id_str)
                # assign a child to a parent
                parent.child = child
                parent.save()
                # assign a parent to a child
                child.parent = parent
                child.save()
            except MyTweet.DoesNotExist:
                pass
        # print("%s child->parent " % i + "MyTweet relationships set")
        return i

    def location_scan(self):
        tweets = MyTweet.objects.filter(screen_name=self.screen_name)  # TODO: filter scanned false
        locations = Location.objects.all()
        for t in tweets:
            for l in locations:
                if l.sub_district.name.title() in t.text:
                    # print("Found possible sub district:")
                    # print(l.sub_district.name.encode("UTF-8"))
                    # print(t.text.encode("UTF-8"))
                    l.mytweet_set.add(t)

    # match tweets to keywords
    def scan(self, keyword_category_str):
        # get MyTweets by the user
        tweets = MyTweet.objects.filter(screen_name=self.screen_name)  # TODO: filter scanned false
        try:
            # get keywords
            keyword_category = KeywordCategory.objects.get(name=keyword_category_str)
            keywords = keyword_category.keyword_set.all()
            for t in tweets:
                for kw in keywords:
                    # TODO: search = re.search('(\s*)(kw)([,.!?\s])', t.text, re.IGNORECASE)
                    if kw.word.upper() in t.text.upper():
                        t.keyword_set.add(kw)
                        t.save()
        except KeywordCategory.DoesNotExist:
            # print("No such category: " + keyword_category_str)
            pass

    # makes models of tweets. if the tweet is a reply, first make a model of that tweet.
    # TODO: reply_to as actual foreign key to another MyTweet object. Just a string for now.
    def make_model(self, tweets):
        created = {}
        for t in tweets:
            try:
                MyTweet.objects.get(twitter_msg_id=t.id_str)
            except MyTweet.DoesNotExist:
                m = MyTweet.objects.create(
                    # msg id is used as the db primary key
                    twitter_msg_id=t.id_str,
                    screen_name=self.screen_name,
                    text=t.text.encode("UTF-8"),
                    # used to assign an object self-reference in models.
                    # save as string
                    reply_to_id_str=t.in_reply_to_status_id_str,
                    created_at=t.created_at,
                )
                created[m.twitter_msg_id] = m
        return created
