from django.http import HttpResponse
from django.template import loader

from twep.models import User


def index(request):
    # ?u=screen_name in the url that runs this code. See twep/urls.py and mysite/urls.py
    sn = request.GET.get('u', '')
    d = ""
    try:
        user = User.objects.get(screen_name=sn)
        template = loader.get_template('present.html')
        if user.blob_data:
            d = user.blob_data
        else:
            d = "Dokument mangler"
    except User.DoesNotExist:
        template = loader.get_template('nothing_found.html')
    context = {
         'markdown': d,
    }
    return HttpResponse(template.render(context))

