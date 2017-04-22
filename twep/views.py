from twep.tweepyImpl import Tweets
from django.http import HttpResponse
from twep.models import MyTweet

# Create your views here.


def index(request):

    return HttpResponse("hello")

