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

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

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

