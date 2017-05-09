import base64

from django.core.management.base import BaseCommand

from twep.models import Timeline, Keyword, Location, User
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
        situations = Timeline.objects.filter(screen_name=sn)
        user = User.objects.get_or_create(screen_name=sn)[0]
        for sit in situations:
            title = sit.first_tweet.twitter_msg_id
            if sit.first_tweet.text_summary_title:
                title += " - " + sit.first_tweet.text_summary_title
            mark.header_1(title)
            mark.text(sit.first_tweet.text, bold=True)
            for t in sit.first_tweet.get_all_children(include_self=False):
                mark.text(t.text, italic=True)
                mark.timestamp(t.created_at)
                if t.categories_keywords:
                    kc = mark.List("Categories:")
                    for k, v in t.categories_keywords.items():
                        kc.unordered_entry(k.name, indentation=1)
                    kc.make()
                # try:
                #     if t.text_summary:
                #         mark.header_4("Summary: ")
                #         mark.header_5(t.text_summary)
                # except TypeError:
                #     pass
                md_list = mark.List("Possible location: ")
                try:
                    l = Location.objects.get(tweet=t)
                    md_list.unordered_entry(l.sub_district.name, indentation=1).make()
                except Location.DoesNotExist:
                    pass
            user.blob_data = mark.md_str
            user.save()
