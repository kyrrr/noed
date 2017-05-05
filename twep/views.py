from django.http import HttpResponse
from django.template import loader

from twep.util.tweets import tweetmarker


def index(request):
    sn = request.GET.get('u', '')
    d = tweetmarker.mark_tweets_by(sn)
    if len(d) <= 1:
        template = loader.get_template('nothing_found.html')
    else:
        template = loader.get_template('present.html')
    context = {
        'markdown': d,
    }
    return HttpResponse(template.render(context))

