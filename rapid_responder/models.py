from django.db import models
from django.forms import ModelForm
from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from datetime import datetime, date
from pytz import timezone
from django.core.exceptions import ValidationError
from django.forms import CharField, PasswordInput, Form
from django.contrib.auth.models import User

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
    conditions = models.ManyToManyField(Condition, on_delete=models.SET_NULL, related_name="patients")


