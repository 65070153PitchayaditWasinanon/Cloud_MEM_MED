from django.shortcuts import render, redirect
from django.db.models import *
from django.db.models.functions import *
from django.db.models.lookups import *
from .models import *
from django.http import JsonResponse
from django.http import HttpResponse
from django.views import View
from calendar import HTMLCalendar
from datetime import datetime
from django.shortcuts import render
import calendar as cale

#import จาก forms.py ด้านล่างนี้
from MEM_MED.forms import AddMedicineForm, AddDailyMedicineForm

class daily_medicine_detail(View):

    def get(self, request):
        return render(request, 'dailymedicinedetail.html', {"form":1, "teacher":2})


class calendar(View):
    
    def get(self, request, year=None, month=None):
        log = MedicationLog.objects.all()

        if year is None or month is None:
            now = datetime.now()
            year = now.year
            month = now.month
        else:
            year = int(year)
            month = int(month)

        cal = cale.Calendar()
        month_days = cal.monthdayscalendar(year, month)

        log_dates = {log.date_taken.day for log in log if log.date_taken.year == year and log.date_taken.month == month and log.missed == None}
        log_dates_missed = {log.date_taken.day for log in log if log.date_taken.year == year and log.date_taken.month == month and log.missed == True}
        log_dates_not_missed = {log.date_taken.day for log in log if log.date_taken.year == year and log.date_taken.month == month and log.missed == False}
        
        if month == 1:
            prev_month = 12
            prev_year = year - 1
        else:
            prev_month = month - 1
            prev_year = year


        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year

        return render(request, 'calendar.html', {
            'month_days': month_days,
            'year': year,
            'month': month,
            'month_name': cale.month_name[month],
            'prev_year': prev_year,
            'prev_month': prev_month,
            'next_year': next_year,
            'next_month': next_month,
            'log_dates': log_dates, 
            'log_dates_missed': log_dates_missed,
            'log_dates_not_missed': log_dates_not_missed
        })

def day_view(request, year, month, day):
    return HttpResponse(f"You clicked on {day}/{month}/{year}")

class MedicineAddView(View):
    def get(self, request):

        medication_target = Medication.objects.all()
        form = AddMedicineForm()
        return render(request, 'add-medicine.html', {"medication_target" : medication_target, "form" : form})
    
    def post(self, request):

        medication_target = Medication.objects.all()
        form = AddMedicineForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("add-medicine")
        else:
            return render(request, 'add-medicine.html', {"medication_target" : medication_target, "form" : form})

class MedicineDeleteView(View):

    def get(self, request, pk):
        medication_target = Medication.objects.get(pk=pk)
        medication_target.delete()
        return redirect('add-medicine')

class MedicineEditView(View):

    def get(self, request, pk):
        medication_target = Medication.objects.get(pk=pk)
        form = AddMedicineForm(instance=medication_target)
        return render(request, 'edit-medicine.html', {"form" : form})

    def post(self, request, pk):

        medication_target = Medication.objects.get(pk=pk)
        form = AddMedicineForm(request.POST, request.FILES, instance=medication_target)

        if form.is_valid():
            form.save()
            return redirect("add-medicine")
        else:
            print(form.errors)
            form = AddMedicineForm(instance=medication_target)
            return render(request, 'edit-medicine.html', {"form" : form})

class DailyMedicineAddView(View):
    def get(self, request):

        medication_schedule_target = MedicationSchedule.objects.all()
        form = AddDailyMedicineForm()
        return render(request, 'add-daily-medicine.html', {"medication_schedule_target" : medication_schedule_target, "form" : form})
    
    def post(self, request):

        medication_schedule_target = MedicationSchedule.objects.all()
        form = AddDailyMedicineForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("add-daily-medicine")
        else:
            return render(request, 'add-daily-medicine.html', {"medication_schedule_target" : medication_schedule_target, "form" : form})