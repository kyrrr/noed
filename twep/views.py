from django.shortcuts import render
from twep.tweepyImpl import UserTweetsThing
from twep.scraper import Scraper
from twep.settings import KEYWORDS
from django.http import HttpResponse
from twep.models import MyTweet
from twep.scraper import Scraper
import pprint
import inspect


# Create your views here.

def index(request):
    #i = UserTweetsThing()
    u = 'oslopolitiops'
    s = Scraper()
    #nt = i.get_newest(username=u, count=5)
    #i.make_model(u, nt)
    bu = MyTweet.objects.filter(screen_name=u)
    for t in bu:
        #s.scan_category(KEYWORDS[0]['DANGER'], t.text)
        print(type(bytearray(t.text.encode("UTF-8"))))
    return HttpResponse("ser")
