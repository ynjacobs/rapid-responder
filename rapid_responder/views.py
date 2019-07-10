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
import json

def home(request):
    return JsonResponse({"hello": "world"})

def save_res(request):
    # uname = request.POST['uname']

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    uname = body['uname']
    fname = body['fname']
    lname = body['lname']
    email = body['email']
    phone = body['phone']
    pwd = body['password']
    quals = body['quals']

    user = User.objects.create_user(uname, email, pwd,first_name=fname, last_name=lname)
    profile = Profile()
    profile.user = user
    profile.flag = 'R'
    profile.save()

    responder = Responder()
    responder.profile = profile
    responder.phone_number = phone
    responder.name = f'{fname} {lname}'
    responder.save()
    for id in quals:
        qual = Qualification.objects.get(pk=id)
        responder.qualifications.add(qual)
    responder.save()
    login(request, user)
    signer = Signer()
    signedText = signer.sign(f'{uname} {pwd}')
    response = JsonResponse({"hello": "world"})
    # response.set_cookie('rr_auth', signedText) 
    response.set_cookie('rr_auth', signedText) 

    return response

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

    