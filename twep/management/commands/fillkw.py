import datetime
import sys
from django.core.management.base import BaseCommand
from twep.models import Keyword, KeywordCategory, Location, City, District, SubDistrict
import twep.keywords


class Command(BaseCommand):

    help = 'Run to insert keywords and categories into db. Read from in keywords.py'
    get_no_more_than = 1000
    kws = twep.keywords.kws  # from keywords.pye
    locs = twep.keywords.location_kws

    def handle(self, *args, **options):

        # HACKY
        if input("Add locations (Oslo) to database? (y or anything else to cancel)") == "y":
            for key, value in self.locs["oslo"].items():
                try:
                    c = City.objects.get(name="oslo")
                except City.DoesNotExist:
                    c = City.objects.create(name="oslo")

                for district, subdistricts in value.items():
                    try:
                        d = District.objects.get(city=c, name=district)
                    except District.DoesNotExist:
                        d = District.objects.create(city=c, name=district)

                    for sd in subdistricts:
                        try:
                            s = SubDistrict.objects.get(district=d, name=sd)
                        except SubDistrict.DoesNotExist:
                            s = SubDistrict.objects.create(district=d, name=sd)

                        try:
                            Location.objects.get(
                                city=c,
                                district=d,
                                sub_district=s
                            )
                        except Location.DoesNotExist:
                            print(s.name.encode("UTF-8"))
                            Location.objects.create(
                                city=c,
                                district=d,
                                sub_district=s
                            )

        if input("Add keywords to database? (y or anything else to cancel)") == "y":
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
        print("Bye bye")

