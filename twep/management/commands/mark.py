import base64

from django.core.management.base import BaseCommand

from twep.models import Situation, Keyword, Location, User
from twep.util.text import markdown


class Command(BaseCommand):

    # help = 'Print stuff by username to a log file using > or >> in terminal'

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)

    # holy fucking loops batman wtf
    # this cannot be healthy
    def handle(self, *args, **options):
        sn = options['screen_name']
        mark = markdown.MarkDown()
        mark.header_1(sn)
        situations = Situation.objects.filter(screen_name=sn)
        user = User.objects.get_or_create(screen_name=sn)[0]
        for sit in situations:
            tweets = sit.first_tweet.get_all_children(include_self=True)
            mark.header_2(sit.first_tweet.twitter_msg_id)
            for t in tweets:
                mark.text(t.text, italic=True)
                md_list = mark.List("Mulig sted:")
                try:
                    l = Location.objects.get(mytweet=t)
                    md_list.unordered_entry(l.sub_district.name).make()
                except Location.DoesNotExist:
                    pass
                try:
                    ftkws = Keyword.objects.filter(tweets=t)
                    kwmdl = mark.List("Keywords:")
                    for kw in ftkws:
                        kwmdl.unordered_entry(kw.category.name)
                        kwmdl.unordered_entry(kw.word, indentation=1)
                    kwmdl.make()
                except Keyword.DoesNotExist:
                    mark.text("No keywords found for " + t.twitter_msg_id)
                    pass
            user.blob_data = mark.md_str
            user.save()
