import pprint
import inspect
from collections import defaultdict
from twep.settings import KEYWORDS
from twep.models import MyTweet, Keyword, Situation


class TweetTransformer:
    # test data
    # violation_keywords = ['avskiltes', 'fratas', 'fratatt', 'tagger', 'tagging']
    # good_keywords = ['ingen personskade', 'reddet', 'funnet']
    # danger_keywords = ['røykutvikling', 'knivstukket', 'kniv', 'våpen', 'brann', 'stjålet', 'saknet', 'savnet', 'skudd']
    # status_keywords = ['melding om', 'er fremme' 'er på stedet', 'på vei til stedet',\
    #     'slukket', 'pågrepet', 'i arrest', 'tatt vare på']
    # preposition_keywords = ['i', 'på']
    # street_keywords = ['veien', 'gate']

    keywords = None
    screen_name = None

    # TODO: use these booleans to guarantee an order to things?
    # situated = False
    # pc_set = False
    # scanned = False

    def __init__(self, screen_name):
        self.keywords = KEYWORDS[0]
        self.screen_name = screen_name

    # places tweets in a "situation" object, in the order they were tweeted
    def situate(self):
        # parent null, child notnull
        # the first part of a series
        orphans_with_children = MyTweet.objects.filter(screen_name=self.screen_name)\
            .filter(child__isnull=False)\
            .filter(parent__isnull=True)\
            # .filter(situation__isnull=True)
        created = []
        for oc in orphans_with_children:
            exists = Situation.objects.filter(base_tweet=oc)
            if len(exists) > 0:
                continue
            else:
                created.append(Situation.objects.create(base_tweet=oc))
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
        # print("Parent child set")

    # match tweets to keywords
    def scan(self, category):
        # get MyTweets by the user
        tweets = MyTweet.objects.filter(screen_name=self.screen_name)  # .filter(twitter_msg_id="852661744384303105")
        # get keywords
        keywords = Keyword.objects.filter(category=category)
        for t in tweets:
            for kw in keywords:
                if kw.word in t.text:
                    t.keyword.add(kw)
                    t.save()
