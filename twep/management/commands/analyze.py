from collections import defaultdict
from django.core.management.base import BaseCommand

from twep.models import Timeline, Keyword, Location, User, Tweet, KeywordCategory
from twep.util.text import markdown


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('screen_name', type=str)

    # holy fucking loops batman wtf
    # this cannot be healthy
    def handle(self, *args, **options):
        sn = options['screen_name']
        tweets = Tweet.objects.filter(screen_name=sn)
        for t in tweets:
            danger = 0
            safety = 0
            good_guy = 0
            bad_guy = 0
            in_progress = 0
            resolved = 0
            victim = 0
            traffic = 0
            damage = 0
            taking_action = 0
            accidents = 0
            fire = 0
            residence = 0
            vehicle = 0
            missing = 0
            call_to_action = 0
            weapon = 0
            crime = 0
            summary_title = ""
            summary = ""
            categories_keywords = t.categories_keywords
            if categories_keywords:
                for ckw in categories_keywords:
                    # STATUS
                    if ckw.name == 'in_progress':
                        in_progress += 1

                    if ckw.name == 'resolved':
                        resolved += 1

                    # CRIME
                    if ckw.name == 'weapon':
                        weapon += 1
                    if ckw.name == 'crime':
                        crime += 1

                    # PEOPLE
                    if ckw.name == 'good_guy':
                        good_guy += 1
                    if ckw.name == 'bad_guy':
                        bad_guy += 1
                    if ckw.name == 'victim':
                        victim += 1

                    # TRAFFIC
                    if ckw.name == 'accidents':
                        accidents += 1
                    if ckw.name == 'traffic_information':
                        traffic += 1

                    if ckw.name == 'damage':
                        damage += 1
                    if ckw.name == 'taking_action':
                        taking_action += 1
                    if ckw.name == 'fire':
                        fire += 1
                    if ckw.name == 'call_to_action':
                        call_to_action += 1
                    if ckw.name == 'missing':
                        missing += 1
                    if ckw.name == 'residence':
                        residence += 1

                    # STRING
                    # try to make string...
                    # TITLE
                    if fire == 1:
                        summary_title = "fire "
                    if accidents == 1:
                        summary_title = "accident "
                    if crime == 1:
                        summary_title = "crime "
                    if in_progress > resolved:
                        summary_title += "in progress"
                    elif resolved > in_progress:
                        summary_title += "resolved"
                    if traffic == 1:
                        summary_title = "traffic situation "

                    # TEXT
                    if bad_guy > 0:
                        summary += "bad guy "
                    if good_guy > 0:
                        summary += "good guy "
                    if weapon > 0:
                        summary += "weapon "
                    if call_to_action > 0:
                        summary += "asking public "
                    if missing > 0:
                        summary += "something missing "
                    if victim > 0:
                        summary += "someone hurt "
            t.text_summary_title = summary_title
            t.text_summary = summary
            t.save()


