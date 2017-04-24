import pprint
import inspect
from twep.settings import KEYWORDS
from twep.models import MyTweet, Keyword, Situation


class Scraper:
    # test data
    violation_keywords = ['avskiltes', 'fratas', 'fratatt']
    good_keywords = ['ingen personskade', 'reddet', 'funnet']
    # danger_keywords = ['røykutvikling', 'knivstukket', 'kniv', 'våpen', 'brann', 'stjålet', 'saknet', 'savnet', 'skudd']
    status_keywords = ['melding om', 'er fremme' 'er på stedet', 'på vei til stedet', 'slukket', 'pågrepet', 'i arrest', 'tatt vare på']
    preposition_keywords = ['i', 'på']
    street_keywords = ['veien', 'gate']

    keywords = None

    screen_name = None

    def __init__(self, screen_name):
        self.keywords = KEYWORDS[0]
        self.screen_name = screen_name

    def situate(self):
        # parent null, child notnull
        # the first part of a series
        orphans_with_children = MyTweet.objects.filter(screen_name=self.screen_name)\
            .filter(child__isnull=False)\
            .filter(parent__isnull=True)\
            .filter(scanned=False)

        for oc in orphans_with_children:
            s = Situation()
            s.save()
            s.mytweet_set.add(oc)
            # print(oc.twitter_msg_id)
            # print(oc.text)
            children = MyTweet.get_all_children(oc)
            # print(children)
            for c in children:
                s.mytweet_set.add(c)
                s.mytweet_set.add()
                # print(c.text)
            s.save()
            print(s.mytweet_set.all()[0].text)

    # assigns parent and child to tweets
    def set_reply_timeline(self):
        not_scanned = MyTweet.objects.filter(screen_name=self.screen_name).filter(scanned=False)
        are_replies = not_scanned.filter(reply_to_id_str__isnull=False)\
            # .filter(parent__isnull=True)  # uncomment and append to not include those that have a timeline set. MAYBE
        # keep it this way now for testing
        for child in are_replies:
            try:
                parent = MyTweet.objects.get(twitter_msg_id=child.reply_to_id_str)
                parent.child = child
                parent.save()
                child.parent = parent
                child.save()
                # print(child.text.encode("UTF-8"))
                # print("is self-reply (@" + self.screen_name + ") to")
                # print(parent.text.encode("UTF-8"))
            except MyTweet.DoesNotExist:
                # print("No parent for " + child.twitter_msg_id)
                pass

    # figure out what is to be scanned for in a tweet
    # currently implemented:
    #     Jackity Shit
    def scan(self, tweet_id, categories=None):
        try:
            tweet = MyTweet.objects.get(twitter_msg_id=tweet_id)
        except MyTweet.DoesNotExist:
            print("Tweet does not exist! Byebye")
            return
        if categories is None:
            print("scan for all")
            print("scan for all is not yet implemented!!")
            return
        res = []
        for c in categories:
            if c.upper() is 'DANGER':
                res.append(self.scan_danger(tweet.text))

    # match a tweet to the list of spooky bad keywords
    def scan_danger(self, text):
        found = []
        for dkw in self.keywords['DANGER']:
            if dkw in text:
                print("/!\\DANGER DANGER/!\\")
                print("Found: " + dkw)
                print("In text: ")
                print(text)
                found.append(dkw)
        return found

    def scan_location(self, text):
        pass
