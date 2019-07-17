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
            # print("serialized_user:",serialized_user.data)
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
    permission_classes = [AllowAny]

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
        address = body['address']
        medications = body['medications']
        emer_contact_name = body['emer_contact_name']
        emer_contact_number = body['emer_contact_number']
        pwd = body['password']

        conds = body['conds']
        print('conds:::::', conds)

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
        patient.address = address
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
    

        return Response({'message':'Success'})

class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = [AllowAny,]

    def update(self, request, pk=None):
        print("in update with pk:", pk)
        body = request.data
        res_id = body['res_id']
        print("in update with request params:", res_id)

        responder = Responder.objects.get(id=res_id)
        case = Case.objects.get(pk=pk)
        print("responder:", responder)        
        case.responder = responder
        case.status = Case.ONGOING
        case.save()

        data = self.serializer_class(case).data if case else None
        print("serialized_cases", data)
        return Response({'message':'Success, almost!', "case": data})

    def create(self, request):
        body = request.data
        patient = body['patient']
        condition = body['condition']
        description = body['description']

        print("patient:", patient["id"])
        print("condition:", condition)
        print("description:", description)

        case = Case()
        case.patient = Patient.objects.get(pk=patient["id"])

        case.condition = Condition.objects.get(pk=condition["id"])
        case.description = description
        case.save()
        
        serialized_case = self.serializer_class(case)
        data = serialized_case.data

        return Response({'message':'Success', "case": data})

    @action(methods=['get'], detail=True, url_path='ongoing', url_name='ongoing')
    def get_ongoing_case_by_resname(self, request, pk=None):
        print("in get_ongoing_case_by_resname")
        print("::: ", request, pk)
        responder = Responder.objects.get(id=pk)
        cases = Case.objects.all().filter(status=Case.ONGOING).filter(responder=responder)
        data = None
        if cases and len(cases) > 0:
            case = cases[0]
            serialized_case = self.serializer_class(case)
            data = serialized_case.data

        print("serialized_case", data)
        return Response({'message':'just welcome', 'case': data })

    @action(methods=['get'], detail=False, url_path='unassigned', url_name='unassigned')
    def get_unassigned_cases(self, request):
        print("in get_unassigned_cases")
        cases = Case.objects.filter(status=Case.UNASSIGNED)
        data = None
        if cases and len(cases) > 0:
            serialized_cases = self.serializer_class(cases, many=True)
            data = serialized_cases.data

        print("serialized_cases", data)
        return Response({'cases': data })

    @action(methods=['get'], detail=True, url_path='get_unassign_cases_pat', url_name='get_unassign_cases_pat')
    def get_unassign_cases_by_patname(self, request, pk=None):
        print("in get_unassign_cases_by_patname")
        print("::PK::", pk)
        patient = Patient.objects.get(id=pk)
        cases = Case.objects.all().filter(status__in=[Case.UNASSIGNED, Case.ONGOING]).filter(patient=patient)
        data = None
        if cases and len(cases) > 0:
            case = cases[0]
            serialized_case = self.serializer_class(case)
            data = serialized_case.data

        print("serialized_case", data)
        return Response({'message':'just welcome', 'case': data })

class QualViewSet(viewsets.ModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualSerializer
    permission_classes = [AllowAny,]

class CondViewSet(viewsets.ModelViewSet):
    queryset = Condition.objects.all()
    serializer_class = CondSerializer
    permission_classes = [AllowAny,]

