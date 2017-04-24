from django.http import HttpResponse
from twep.models import *

# Create your views here.


def index(request):
    a = MyTweet.objects.filter(screen_name__exact='kyrrelicious')
    k = a.filter(reply_to__isnull=False)
    print(k)
    for f in k:
        print(f.text.encode("UTF-8"))
    return HttpResponse("hello")

