import json

from django.shortcuts import render_to_response, redirect, RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.views import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login as _login


def landing(request):
    return render_to_response('landing.html', {}, RequestContext(request))


def home(request):
    if not request.user.is_authenticated():
        return redirect(reverse('landing'))
    else:
        return render_to_response('game_application.html', {'user': request.user}, RequestContext(request))


def login(request):
    if request.method == "POST":
        data = request.POST or json.loads(request.body)
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user is not None:
            if user.is_active:
                _login(request, user)
                return redirect(reverse('home'))
            else:
                errors = 'Your user account is not active'
        else:
            errors = 'Your username and password do not match our records'
        return render_to_response('login.html', {
            'errors': errors
        }, RequestContext(request))
    else:
        return render_to_response('login.html', {}, RequestContext(request))


def logout_user(request):
    logout(request)
    return redirect(reverse('login'))