import time
import re
from twep.models import MyTweet, Keyword, KeywordCategory, Situation


class TweetTransformer:

    screen_name = None

    # TODO: use booleans to guarantee an order to things? Meh

    def __init__(self, screen_name):
        self.screen_name = screen_name

    def get_latest(self):
        return MyTweet.objects.filter(screen_name=self.screen_name).latest('created_at')

    # places tweets in a "situation" object, in the order they were tweeted
    # also picks up single tweets BAD IDEA
    def make_situation(self):
        user_tweets = MyTweet.objects.filter(screen_name=self.screen_name)
        # orphans_with_children = MyTweet.objects.filter(screen_name=self.screen_name)\
            # .filter(child__isnull=False)\
            # .filter(parent__isnull=True)
        # print("Found %s" % orphans_with_children.count() + " base tweets for " + self.screen_name)
        created = {}
        for ut in user_tweets:
            if MyTweet.is_orphan_with_child(ut) or MyTweet.is_orphan(ut):
                try:
                    Situation.objects.get(base_tweet=ut)
                except Situation.DoesNotExist:
                    s = Situation.objects.create(screen_name=ut.screen_name, base_tweet=ut)
                    c = MyTweet.get_all_children(ut, include_self=False)
                    s.children = c
                    created[s.id] = s
        print("created %s" % len(created) + " new situations for " + self.screen_name)
        exit()
        return created

    # assigns parent and child to tweets
    def set_parent_child(self):
        not_scanned = MyTweet.objects.filter(screen_name=self.screen_name)
        are_replies = not_scanned.filter(reply_to_id_str__isnull=False)
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
                # print("No parent for " + child.twitter_msg_id)
                pass
        print("%s child->parent " % i + "MyTweet relationships set")

    def location_scan(self, tweets):
        f = KeywordCategory.objects.get(name='location')
        print(f.keyword_set)
        pass

    # match tweets to keywords
    def scan(self, keyword_category_str):
        # get MyTweets by the user
        tweets = MyTweet.objects.filter(screen_name=self.screen_name)  # .filter(twitter_msg_id="852661744384303105")
        # print("Tweets without keywords: %s" % tweets.count())
        # get keywords
        if keyword_category_str == 'location':  # TODO: CONSTS!!
            self.location_scan(tweets)
        else:
            try:
                keyword_category = KeywordCategory.objects.get(name=keyword_category_str)
                keywords = keyword_category.keyword_set.all()
                # print("search for " + keyword_category_str)
                for t in tweets:
                    # print(t.text.encode("UTF-8"))
                    for kw in keywords:
                        # search = re.search('(\s*)(kw)([,.!?\s])', t.text, re.IGNORECASE)
                        if kw.word.upper() in t.text.upper():
                            t.keyword_set.add(kw)
                            t.save()
                            print(t.twitter_msg_id + " has keyword: ")
                            print(kw.word.encode("UTF-8"))
            except KeywordCategory.DoesNotExist:
                print("No such category: " + keyword_category_str)

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
                print("Create " + m.twitter_msg_id)
                created[m.twitter_msg_id] = m
        print("Created %s MyTweets" % len(created))
        return created
