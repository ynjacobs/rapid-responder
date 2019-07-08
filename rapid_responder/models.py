from django.db import models
from django.forms import ModelForm
from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from datetime import datetime, date
from pytz import timezone
from django.core.exceptions import ValidationError
from django.forms import CharField, PasswordInput, Form
from django.contrib.auth.models import User
from enum import Enum

class CASE_STATUS(Enum):
    UNASSIGNED = 'unassigned'
    ONGOING = 'ongoing'
    CLOSED = 'closed'
    NOSERVICE = 'noservice'

class STATUS(Enum):
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"

class Condition(models.Model):
    name = models.CharField(max_length=255)
    
class Qualification(models.Model):
    name = models.CharField(max_length=255)

class Patient(models.Model):
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    weight = models.CharField(max_length=255)
    height = models.CharField(max_length=255)
    medications = models.TextField(max_length=2000)
    emer_contact_name = models.CharField(max_length=255)
    emer_contact_number = models.CharField(max_length=255)
    conditions = models.ManyToManyField(Condition,related_name='patients')

class Schedule(models.Model):
    date = models.DateField(default=date.today)
    time_from = models.TimeField()
    time_to = models.TimeField()
    status = models.CharField(max_length=10, default=STATUS.GREEN, choices=[(tag.value, tag.name) for tag in STATUS])

class Responder(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    qualifications = models.ManyToManyField(Qualification,related_name='responders')

class Case(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField()
    status = models.CharField(max_length=20, default=CASE_STATUS.UNASSIGNED, choices=[(tag.value, tag.name) for tag in CASE_STATUS])
    description = models.TextField(max_length=1000)
    condition = models.ForeignKey(Condition, on_delete=models.SET_NULL, null=True, related_name='cases')
    qualification = models.ForeignKey(Qualification, on_delete=models.SET_NULL, null=True, related_name='cases')
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, related_name='cases')
    responder = models.ForeignKey(Responder, on_delete=models.SET_NULL, null=True, related_name='cases')









