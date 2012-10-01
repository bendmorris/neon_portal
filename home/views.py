from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import logout as auth_logout

def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))
def logout(request):
    auth_logout(request)
    return redirect('/')
