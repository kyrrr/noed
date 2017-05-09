import time
import re

from collections import defaultdict

from twep.models import Tweet, Keyword, KeywordCategory, Timeline, Location


class TweetTransformer:

    def __init__(self, screen_name, verbose=False):
        self.screen_name = screen_name
        self.verbose = verbose
        self.vprint = print if self.verbose else lambda *a, **k: None

    def get_latest(self):
        return Tweet.objects.filter(screen_name=self.screen_name).latest('created_at')

    # places tweets in a "situation" object, in the order they were tweeted
    # also picks up single tweets which is not a bad idea
    def make_timeline(self):
        user_tweets = Tweet.objects.filter(screen_name=self.screen_name)  # TODO: filter scanned false
        self.vprint("%s" % user_tweets.count() + " to be put in Situations " + self.screen_name)
        created = {}
        for ut in user_tweets:
            # is the tweet either a parent without a parent, or a "lonely" object
            # it can form the base of a "situation"
            # if MyTweet.is_orphan_with_child(ut) or MyTweet.is_alone(ut):
            if Tweet.is_first_in_series(ut):
                s = Timeline.objects.get_or_create(
                    screen_name=ut.screen_name,
                    first_tweet=ut
                )
                # s[1] is a boolean, true if created - false if gotten. I don't care about those,
                # just make sure all situations are updated
                s_obj = s[0]
                for c in Tweet.get_all_children(ut, include_self=False):
                    s_obj.children.add(c)
                created[s_obj.id] = s_obj
        # we have to ensure the newest tweets also get in, so just scan everything...
        # probably we will not have 1000 tweets to care about "in production"
        self.vprint("Found or created %s" % len(created) + " new timelines for " + self.screen_name)
        return created

    # assigns parent and child to tweets
    def set_child_parent(self):
        tweets = Tweet.objects.filter(screen_name=self.screen_name)  # TODO: filter scanned false
        are_replies = tweets.filter(reply_to_id_str__isnull=False)
        i = 0
        j = 0
        for i, child in enumerate(are_replies):
            try:
                # find the tweet that was replied to
                parent = Tweet.objects.get(twitter_msg_id=child.reply_to_id_str)
                # assign a child to a parent
                parent.child = child
                parent.save()
                # assign a parent to a child
                child.parent = parent
                child.save()
                j += 1
            except Tweet.DoesNotExist:
                pass
        self.vprint("%s child->parent " % j + "Tweet relationships set")
        return i

    def group_keywords(self):
        user_timelines = Timeline.objects.filter(screen_name=self.screen_name)
        if user_timelines.count() < 1:
            print("No timelines found.")
            return
        category_keywords = defaultdict(list)
        for timeline in user_timelines:
            tweets = timeline.first_tweet.get_all_children(include_self=True)
            for t in tweets:
                category_keywords.setdefault(t, {})
                keyword_categories = t.keywordcategory_set.all()
                for kwc in keyword_categories:
                    keywords = t.keyword_set.all()
                    for kw in keywords:
                        if kw.category == kwc:
                            self.vprint(t.twitter_msg_id + ": " + kw.word + " in " + kwc.name)
                            category_keywords[t].setdefault(kwc, []).append(kw)
            t.categories_keywords = category_keywords[t]
            self.vprint("Grouped keywords for " + t.twitter_msg_id)
            t.save()

    def location_scan(self):
        tweets = Tweet.objects.filter(screen_name=self.screen_name)  # TODO: filter scanned false ?
        locations = Location.objects.all()
        for t in tweets:
            for l in locations:
                if l.sub_district.name.title() in t.text:
                    self.vprint("Found possible sub district:")
                    self.vprint(l.sub_district.name)
                    self.vprint(t.text)
                    l.tweet_set.add(t)

    # match tweets to keywords
    def scan(self, keyword_category_str):
        # get MyTweets by the user
        tweets = Tweet.objects.filter(screen_name=self.screen_name)  # TODO: filter scanned false
        try:
            # get keywords
            keyword_category = KeywordCategory.objects.get(name=keyword_category_str)
            keywords = keyword_category.keyword_set.all()
            for t in tweets:
                for kw in keywords:
                    # search = re.search('(\s*|\W*)(' + kw.word + ')(\s*|\W*)', t.text, re.IGNORECASE)
                    # if search:
                    if kw.word.upper() in t.text.upper():
                        self.vprint(kw.word + " in " + t.twitter_msg_id)
                        # mark_key = re.compile(re.escape(kw.word), re.IGNORECASE)
                        # t.text = mark_key.sub("__" + kw.word + "__", t.text)
                        t.keyword_set.add(kw)
                        t.keywordcategory_set.add(kw.category)
                        t.save()
        except KeywordCategory.DoesNotExist:
            self.vprint("No such category: " + keyword_category_str)
            pass

    # makes models of tweets. if the tweet is a reply, first make a model of that tweet.
    def make_model(self, tweets):
        created = {}
        for t in tweets:
            try:
                Tweet.objects.get(twitter_msg_id=t.id_str)
            except Tweet.DoesNotExist:
                m = Tweet.objects.create(
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
