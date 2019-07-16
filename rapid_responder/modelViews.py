from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from rapid_responder.models import *
from rapid_responder.serializers import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.signing import Signer
from django.http import JsonResponse
from django.core import serializers
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated, AllowAny



class ListUsers(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer

    def get(self, request, format=None):
            auth_user = request.user.id
            profile = Profile.objects.get(user=auth_user)
            user = None
            if profile.flag == 'P':
                user = Patient.objects.get(profile=profile)
                serialized_user = PatientSerializer(user)
            else:
                user = Responder.objects.get(profile=profile)
                serialized_user = ResponderSerializer(user)

            print("serialized_user:",serialized_user.data)
            return Response({"user": serialized_user.data})

# @api_view(['POST'])
# @action(methods=['POST'], detail=False, url_path='login', url_name='login')
# def login(request):
#     body = request.data
#     print(body['password'])
#     print(body['uname'])
#     return Response({"message": "Hello, world!"})

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]
    # permission_classes=[AllowAny]

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        body = request.data
        uname = body['uname']
        fname = body['fname']
        lname = body['lname']
        email = body['email']
        age = body['age']
        phone = body['phone_number']
        height = body['height']
        weight = body['weight']
        medications = body['medications']
        emer_contact_name = body['emer_contact_name']

        emer_contact_number = body['emer_contact_number']
        pwd = body['password']
        conds = body['conds']

        user = User.objects.create_user(uname, email, pwd,first_name=fname, last_name=lname)
        profile = Profile()
        profile.user = user
        profile.flag = 'P'
        profile.save()

        patient = Patient()
        patient.profile = profile
        patient.phone_number = phone
        patient.medications = medications
        patient.height = height
        patient.weight = weight
        patient.age = age
        patient.emer_contact_name = emer_contact_name
        patient.emer_contact_number = emer_contact_number
        patient.name = f'{fname} {lname}'

        patient.save()
        for id in conds:
            cond = Condition.objects.get(pk=id)
            patient.conditions.add(cond)
        patient.save()
        login(request, user)

        return Response({'Hello':'World'})

"""
    @action(methods=['POST'], detail=False, url_path='get_p', url_name='get_p')
    def get_patient_byname(self, request):
        print("get_patient_byname")
        print("dddd", request.user.id)
        user = get_object_or_404(User, username=request.data['username'])
        print("11111111111", user)
        
        profile = get_object_or_404(Profile, user=user)
        print("22222222", profile)

        serialized_object = None
        if(profile.flag == 'P'):
            object = get_object_or_404(Patient, profile=profile)
            serialized_object = PatientSerializer(object)    
        else:
            object = get_object_or_404(Responder, profile=profile)
            serialized_object = ResponderSerializer(object)    

        print("3333", serialized_object.data)
 
        return Response({'welcome':'just welcome'})
"""


class ResponderViewSet(viewsets.ModelViewSet):
    queryset = Responder.objects.all()
    serializer_class = ResponderSerializer

    def create(self, request):
        body = request.data
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
    

        return Response({'Hello':'Success'})

