import time
from twep.models import MyTweet, Keyword, KeywordCategory, Situation


class TweetTransformer:

    screen_name = None

    # TODO: use booleans to guarantee an order to things? Meh

    def __init__(self, screen_name):
        self.screen_name = screen_name

    def get_latest(self):
        return MyTweet.objects.filter(screen_name=self.screen_name).latest('created_at')

    # places tweets in a "situation" object, in the order they were tweeted
    def make_timeline(self):
        # parent null, child notnull
        # the first part of a series
        orphans_with_children = MyTweet.objects.filter(screen_name=self.screen_name)\
            .filter(child__isnull=False)\
            .filter(parent__isnull=True)
        print("Found %s" % orphans_with_children.count() + " base tweets for " + self.screen_name)
        created = []
        for oc in orphans_with_children:
            exists = Situation.objects.filter(base_tweet=oc).count()
            if exists > 0:
                # print("situation based on " + oc.twitter_msg_id + " exists")
                continue
            else:
                Situation.objects.create(base_tweet=oc)
                m = Situation.objects.get(base_tweet=oc)
                created.append(m)
        print("created %s" % len(created) + " new situations for " + self.screen_name)
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
        print("%s child->parent " % i + type(MyTweet).__name__ + " relationships set")

    def location_scan(self, tweets):
        f = KeywordCategory.objects.filter(name='location')
        print(f)
        pass

    # match tweets to keywords
    def scan(self, keyword_category_str):
        # get MyTweets by the user
        tweets = MyTweet.objects.filter(screen_name=self.screen_name)  # .filter(twitter_msg_id="852661744384303105")
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
                        if kw.word in t.text:
                            t.keyword_set.add(kw)
                            t.save()
                            print("Saving keyword:")
                            print(kw.word.encode("UTF-8"))
            except KeywordCategory.DoesNotExist:
                print("No such category")

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
