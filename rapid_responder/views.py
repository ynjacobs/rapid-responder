from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from rapid_responder.models import *  
# from django.contrib.auth import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.signing import Signer
from django.http import JsonResponse
from django.core import serializers

def home(request):
    return JsonResponse({"hello": "world"})

def auto_login(request):

    details = {}
    auth_cookie = request.COOKIES.get('rr_auth')
    signer = Signer()
    if auth_cookie:
        security_token = signer.unsign(auth_cookie)
        security_token_arr = security_token.split(' ')
        username = security_token_arr[0]
        password = security_token_arr[1]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            details['Authenticated'] = True
            details['flag'] = 'R'
            profile = Profile.objects.get(user=user)
            if profile.flag == 'P':
                details['flag'] = 'P'
            details['user'] = user
        else:
            details['Authenticated'] = False
    else:
        details['Authenticated'] = False

    response = JsonResponse(details)
    return response

def get_qual(request):
    quals = Qualification.objects.all()
    data = serializers.serialize("json", quals)
    print(data)
    return JsonResponse(data, safe=False)

    