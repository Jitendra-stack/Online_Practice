from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse
# Create your views here.

def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render({},request))


def redirect_to_home(request):
    return redirect('/home')