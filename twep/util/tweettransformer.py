import time
from twep.models import MyTweet, Keyword, Situation


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
        for child in are_replies:
            try:
                # find the tweet that was replied to
                parent = MyTweet.objects.get(twitter_msg_id=child.reply_to_id_str)
                parent.child = child
                parent.save()
                child.parent = parent
                child.save()
            except MyTweet.DoesNotExist:
                # print("No parent for " + child.twitter_msg_id)
                pass
        print("Parent child set")

    # match tweets to keywords
    def scan(self, category):
        # get MyTweets by the user
        tweets = MyTweet.objects.filter(screen_name=self.screen_name)  # .filter(twitter_msg_id="852661744384303105")
        # get keywords
        keywords = Keyword.objects.filter(category=category)
        print("search for " + category)
        for t in tweets:
            for kw in keywords:
                if kw.word in t.text:
                    t.keyword.add(kw)
                    t.save()

    # makes models of tweets. if the tweet is a reply, first make a model of that tweet.
    # TODO: reply_to as actual foreign key to another MyTweet object. Just a string for now.
    def make_model(self, tweets):
        created = []
        for t in tweets:
            exists = MyTweet.objects.filter(twitter_msg_id=t.id_str).count()
            if exists > 0:
                # exit the loop
                continue
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
            created.append(m)
        return created
