from rest_framework import routers, serializers, viewsets
from rapid_responder.models import Patient, Responder, Profile, Schedule, Case
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','email','password')

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = ('name',)
        depth = 2

class ResponderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responder
        fields = '__all__'
        depth = 2

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        depth = 1

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'
        depth = 1

