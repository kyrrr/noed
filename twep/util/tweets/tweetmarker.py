from twep.models import *
from twep.util.text import markdown


def mark_tweets_by(screen_name):
    mark = markdown.MarkDown()
    situations = Situation.objects.filter(screen_name=screen_name)
    for sit in situations:
        first = sit.first_tweet
        mark.header_1(first.twitter_msg_id) \
            .text(first.text)
        try:
            l = Location.objects.get(mytweet=first)
            mark.header_4("Possible location:") \
                .text(l.sub_district.name)
        except Location.DoesNotExist:
            pass
        try:
            ftkws = Keyword.objects.filter(tweets=first)
            mark.header_4("Keywords:")
            for kw in ftkws:
                mark.text(kw.word)
        except Keyword.DoesNotExist:
            print("No keywords found for " + first.twitter_msg_id)
            pass
        if sit.children.all().count() > 0:
            for i, sc in enumerate(sit.children.all()):
                mark.header_4("Follow-up %s:" % (i + 1))
                mark.text(sc.text)
                try:
                    cl = Location.objects.get(mytweet=sc)

                    mark.header_4("Possible location") \
                        .text(cl.sub_district.name)
                except Location.DoesNotExist:
                    pass

                try:
                    ckws = Keyword.objects.filter(tweets=sc)
                    mark.header_4("Keywords:")
                    for ckw in ckws:
                        mark.text(ckw.word)
                except Keyword.DoesNotExist:
                    # print("No keywords found for " + first.twitter_msg_id)
                    pass
                    # if sc.get_last_parent() and sit.first_tweet == sc.get_last_parent():
                    # pass
    return mark.doc()

