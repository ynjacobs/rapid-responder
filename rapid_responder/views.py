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

def home(request):
    return JsonResponse({"hello": "world"})

# def auto_login(request):

#     details = {}
#     auth_cookie = request.COOKIES.get('rr_auth')
#     signer = Signer()
#     if auth_cookie:
#         security_token = signer.unsign(auth_cookie)
#         security_token_arr = security_token.split(' ')
#         username = security_token_arr[0]
#         password = security_token_arr[1]
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             details['Authenticated'] = True
#             details['flag'] = 'R'
#             profile = Profile.objects.get(user=user)
#             if profile.flag == 'P':
#                 details['flag'] = 'P'
#             details['user'] = user
#         else:
#             details['Authenticated'] = False
#     else:
#         details['Authenticated'] = False

#     response = JsonResponse(details)
#     # response['Access-Control-Allow-Origin'] = 'http://localhost:3000/'
#     # # response["Access-Control-Allow-Origin"] = '*'
#     # # response["Access-Control-Allow-Credentials"] = "true"
#     # # response["Access-Control-Allow-Methods", "GET,HEAD,OPTIONS,POST,PUT"]
#     response['Access-Control-Allow-Methods'] = 'DELETE, GET, OPTIONS, PATCH, POST, PUT'
#     response['Access-Control-Allow-Origin'] = '*'

#     response['Access-Control-Allow-Headers'] = 'access-control-allow-origin, accept, accept-encoding, authorization, content-type, dnt, origin, user-agent, x-csrftoken, x-requested-with'
#     # response["Access-Control-Allow-Headers"] = "Access-Control-Allow-Headers, Origin,Access-Control-Allow-Origin, Access-Control-Request-Headers"
#     # response["Access-Control-Allow-Headers"] = "access-control-allow-origin"
#     return response

    