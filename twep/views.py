from django.http import HttpResponse
from django.template import loader

from twep.util.tweets import tweetmarker


def index(request):
    sn = "oslopolitiops"
    d = tweetmarker.mark_tweets_by(sn)
    template = loader.get_template('present.html')
    context = {
        'markdown': d,
    }
    return HttpResponse(template.render(context))

