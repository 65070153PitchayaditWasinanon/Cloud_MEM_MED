from django import forms
from .models import *
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.forms import ModelForm, SplitDateTimeField
from django.forms.widgets import Textarea, TextInput, SplitDateTimeWidget
from django.core.exceptions import ValidationError
from datetime import datetime, timezone
from django.db import transaction

from django.db import models
from django import forms

from MEM_MED.models import *

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    allergies = forms.CharField(max_length=100)
    medical_history = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'birthdate', 'allergies', 'medical_history']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()  # บันทึกข้อมูล User
            patient_group = Group.objects.get(name='Patient')
            patient_group.user_set.add(user)
        return user

class RegisterDoctorForm(UserCreationForm):
    email = forms.EmailField(required=True)
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    expertise = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'birthdate', 'expertise']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()  # บันทึกข้อมูล User
            doctor_group = Group.objects.get(name='Doctor')
            doctor_group.user_set.add(user)
        return user

class AddMedicineForm(ModelForm):

    class Meta:
        model = Medication
        fields = ["image",
                  "name",
                  "dosage",
                  "description",
                  "side_effects",
                ]

class AddDailyMedicineForm(ModelForm):

    class Meta:
        model = MedicationSchedule
        fields = ["patient",
                  "medication",
                  "time_to_take",
                  "date_to_take",
                  "before_after",
                  "is_eaten",
                  "quantity",
                  "instructions"]
        widgets = {
            'date_to_take': forms.DateInput(attrs={'type': 'date'}),
        }

class MedicationScheduleForm(forms.ModelForm):
    class Meta:
        model = MedicationSchedule
        fields = ['is_eaten']

    def __init__(self, *args, **kwargs):
        super(MedicationScheduleForm, self).__init__(*args, **kwargs)
        self.fields['is_eaten'].widget = forms.HiddenInput()


class Report(forms.ModelForm):
    detail = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "class":"form-control"}))
    class Meta:
        model = SideEffect
        fields = ['date', 'detail']

from django import forms
from .models import DoctorAppointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = DoctorAppointment
        fields = ['appointment_date', 'appointment_time', 'notes']
        widgets = {
            'appointment_date': forms.DateInput(attrs={
                'class': 'form-input', 
                'placeholder': 'YYYY-MM-DD',
                'type': 'date'  # HTML5 date input
            }),
            'appointment_time': forms.TimeInput(attrs={
                'class': 'form-input', 
                'placeholder': 'HH:MM',
                'type': 'time'  # HTML5 time input
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-input notes-textarea', 
                'placeholder': 'Any additional notes'
            }),
        }

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data['appointment_date']

        # Correct the comparison to call .date()
        if appointment_date <= datetime.now(timezone.utc).date():
            raise ValidationError("The appointment date cannot be in the past.")

        return appointment_date

