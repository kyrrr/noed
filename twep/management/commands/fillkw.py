import datetime
import sys
from django.core.management.base import BaseCommand
from twep.models import Keyword, KeywordCategory
import twep.keywords


class Command(BaseCommand):

    help = 'Run to insert keywords and categories into db. Read from in keywords.py'
    get_no_more_than = 1000
    kws = twep.keywords.kws  # from keywords.pye

    def handle(self, *args, **options):

        # OR import/have lists here
        if len(self.kws) < 1:
            print("Nothing to do")
            return

        if input("Set categories? (y or anything else to cancel)") == "y":
            for kwc in self.kws:
                try:
                    KeywordCategory.objects.get(name=kwc)
                except KeywordCategory.DoesNotExist:
                    c = KeywordCategory.objects.create(name=kwc)
                    print("Create category:")
                    print(c.name)
                # for keyword in keywords at keyword category
                for kw in self.kws[kwc]:
                    try:
                        Keyword.objects.get(word=kw)
                    except Keyword.DoesNotExist:
                        try:
                            c = KeywordCategory.objects.get(name=kwc)
                            w = Keyword.objects.create(word=kw)
                            c.keyword_set.add(w)
                            print(w.word.encode("UTF-8"))
                        except KeywordCategory.DoesNotExist:
                            print("cannot add to non-existent category")

        else:
            print("Bye Bye")
            return

