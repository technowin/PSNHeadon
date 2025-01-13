from calendar import day_name, month_name
from decimal import Decimal
from itertools import count
import json
# from tkinter import font
import math
import os
import traceback
from colorama import Cursor
from django.conf import settings
from django.http import FileResponse, JsonResponse
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from pyparsing import str_type
from Account.models import user_role_map
from Masters.models import CityMaster, SlotDetails, StateMaster, UserSlotDetails, company_master, sc_employee_master, site_master
from Masters.serializers import PaySlipSerializer, SalaryGeneratedSerializer
from Payroll.models import payment_details as pay
from PSNHeadon.encryption import decrypt_parameter, encrypt_parameter
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.db.models import Sum
from rest_framework.views import APIView
import pandas as pd
from django.views.generic import ListView
from datetime import datetime
from django.db.models import Case, When
import io
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, NamedStyle
from django.db import connection
import requests
from django.http import JsonResponse
import Db
from datetime import date
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa 
import base64
from io import BytesIO
from PIL import Image
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from django.core.files.base import ContentFile
from xhtml2pdf import pisa
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.db.models import Count


def state_master_index(request):
    try:
        states = StateMaster.objects.all()
        for state in states:
            state.pk = encrypt_parameter(str(state.state_id))
        return render(request, 'Tax/StateMaster/index.html', {'states': states})
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
    
def state_create(request):
    if request.method == 'POST':
        form = StateMasterForm(request.POST)
        if form.is_valid():
            state = form.save(commit=False)  # Don't save to the database yet
            state.created_by = request.user   # Also set updated_by initially
            state.save()  # Now save to the database
            messages.success(request, "State created successfully!")
            return redirect('state_master_index')
        else:
            messages.error(request, "Error creating Salary Element.")
    else:
        form = StateMasterForm()
    return render(request, 'Tax/StateMaster/create.html', {'form': form})

def state_edit(request, pk):
    pk = decrypt_parameter(pk)
    id = get_object_or_404(StateMaster, pk=pk)

    if request.method == 'POST':
        form = StateMasterForm(request.POST, instance=id)
        if form.is_valid():
            state = form.save(commit=False)  # Don't save to the database yet
            state.updated_by = request.user  # Also set updated_by initially
            state.save()  # Now save to the database
            messages.success(request, "State Name Updated successfully!")
            return redirect('state_master_index')
        else:
            messages.error(request, "Error updating Salary Element.")
    else:
        form = StateMasterForm(instance=id)
    
    return render(request, 'Tax/StateMaster/edit.html', {'form': form, 'id': id})

def state_view(request, pk):
    pk = decrypt_parameter(pk)
    state = get_object_or_404(StateMaster, pk=pk)
    return render(request, 'Tax/StateMaster/view.html', {'state': state})


def city_master_index(request, pk):
    pk = decrypt_parameter(pk)
    try:
        cities = CityMaster.objects.filter(state=pk)
        for city in cities:
            city.pk = encrypt_parameter(str(city.id))
        return render(request, 'Tax/CityMaster/index.html', {'cities': cities,'state_id':pk})
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

    
def city_create(request, state_id):
    try:
        if request.method == 'POST':
            form = CityMasterForm(request.POST)
            if form.is_valid():
                city = form.save(commit=False) 
                city.state = get_object_or_404(StateMaster,state_id=state_id)  # Ensure this matches the foreign key field in the model
                city.created_by = request.user  # Set created_by field
                city.save()  # Save the city to the database
                messages.success(request, "City created successfully!")
                return redirect('state_master_index')  
            else:
                messages.error(request, "Error creating City. Please correct the form.")
        else:
            form = CityMasterForm()
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        # Optionally log the error here for debugging purposes

    return render(request, 'Tax/CityMaster/create.html', {'form': form, 'pk': state_id})



def city_edit(request, pk):
    state = request.GET.get('state')
    pk = decrypt_parameter(pk)
    pk = get_object_or_404(CityMaster, pk=pk)

    if request.method == 'POST':
        form = CityMasterForm(request.POST, instance=pk)
        if form.is_valid():
            city = form.save(commit=False) 
            city.state = get_object_or_404(StateMaster,state_id=state) # Don't save to the database yet
            city.updated_by = request.user  # Also set updated_by initially
            city.save()  # Now save to the database

            messages.success(request, "City Name Updated successfully!")
            return redirect('state_master_index')
        else:
            messages.error(request, "Error updating City.")
    else:
        form = CityMasterForm(instance=pk)
    
    return render(request, 'Tax/CityMaster/edit.html', {'form': form, 'pk1': pk,'pk':state})

def city_view(request, pk):
    state = request.GET.get('state')
    pk = decrypt_parameter(pk)
    city = get_object_or_404(CityMaster, pk=pk)
    return render(request, 'Tax/CityMaster/view.html', {'city': city,'pk1':pk ,'pk':state})


def act_master_index(request):
    try:
        acts = ActMaster.objects.all()
        for act in acts:
            act.pk = encrypt_parameter(str(act.act_id))
        return render(request, 'Tax/ActMaster/index.html', {'acts': acts})
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
    
def act_create(request):
    if request.method == 'POST':
        form = ActMasterForm(request.POST)
        if form.is_valid():
            try:
                act = form.save(commit=False)  # Don't save to the database yet
                act.created_by = request.user   # Also set updated_by initially
                act.save()  # Now save to the database
                messages.success(request, "Act created successfully!")
                return redirect('act_master_index')
            except Exception as e:
                return JsonResponse({'message': str(e)}, status=500)
        else:
            messages.error(request, "Error creating Act.")
    else:
        form = ActMasterForm()
    return render(request, 'Tax/ActMaster/create.html', {'form': form})

def act_edit(request, pk):
    pk = decrypt_parameter(pk)
    id = get_object_or_404(ActMaster, pk=pk)

    if request.method == 'POST':
        form = ActMasterForm(request.POST, instance=id)
        if form.is_valid():
            city = form.save(commit=False)  # Don't save to the database yet
            city.updated_by = request.user  # Also set updated_by initially
            city.save()  # Now save to the database
            messages.success(request, "Act Updated successfully!")
            return redirect('act_master_index')
        else:
            messages.error(request, "Error updating Salary Element.")
    else:
        form = ActMasterForm(instance=id)
    
    return render(request, 'Tax/ActMaster/edit.html', {'form': form, 'id': id})

def act_view(request, pk):
    pk = decrypt_parameter(pk)
    act = get_object_or_404(ActMaster, pk=pk)
    return render(request, 'Tax/ActMaster/view.html', {'act': act})


def slab_index(request,pk):
    pk = decrypt_parameter(pk)
    type = request.GET.get('type')
    act = request.GET.get('act_id')
    try:
        slabs = Slab.objects.filter(slab_id = pk, slab_type = type)
        for slab in slabs:
            slab.pk = encrypt_parameter(str(slab.id))
        return render(request, 'Tax/Slab/index.html', {'slabs': slabs,'act':act,'type':type,'slab_id':pk})
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
    

def slab_create(request):
    slab_type = request.GET.get('type')
    act = request.GET.get('act')
    slab_id = request.GET.get('slab_id')

    if request.method == 'POST':
        try:
            # Retrieve POST data
            post_data = {key: request.POST.get(key) or None for key in [
                'effective_date', 'salary_from', 'salary_to', 'salary_deduct', 
                'slab_type','slab_for', 'applicable_designation', 'slab_applicable', 
                'employee_min_amount', 'special_LWF_calculation', 
                'special_employer_contribution', 'employer_min_amount'
            ]}
            post_data['slab_id'] = get_object_or_404(SlabMaster, slab_id=request.POST.get('slab_id'))
            post_data['slab_status'] = 1
            post_data['created_by'] = request.user

            # Save Slab object
            Slab.objects.create(**post_data)
            messages.success(request, "Slab created successfully!")
            return redirect('slab_master_index')
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    # Handle GET request
    context = {
        'slab_type': parameter_master.objects.filter(parameter_name='slab_type'),
        'slab_for': parameter_master.objects.filter(parameter_name='slab_for'),
        'applicable_designation': parameter_master.objects.filter(parameter_name='LWF type'),
        'slab_applicable': parameter_master.objects.filter(parameter_name='slab_applicable'),
        'act': act, 'type': slab_type, 'slab_id': slab_id
    }
    return render(request, 'Tax/Slab/create.html', context)

def slab_edit(request, pk):
    pk = decrypt_parameter(pk)
    slab = get_object_or_404(Slab, id=pk)  # Retrieve the existing slab by its ID

    if request.method == 'POST':
        try:
            # Update slab fields with POST data
            slab.effective_date = request.POST.get('effective_date')
            slab.salary_from = request.POST.get('salary_from')
            slab.salary_to = request.POST.get('salary_to')
            slab.salary_deduct = request.POST.get('salary_deduct')
            slab.slab_type = request.POST.get('type')
            slab.slab_for = request.POST.get('slab_for')
            slab.applicable_designation = request.POST.get('applicable_designation') or None
            slab.slab_applicable = request.POST.get('slab_applicable') or None
            slab.lwf_applicable = request.POST.get('lwf_applicable') or None
            slab.employee_min_amount = request.POST.get('employee_min_amount') or None
            slab.special_LWF_calculation = request.POST.get('special_LWF_calculation') or None
            slab.special_employer_contribution = request.POST.get('special_employer_contribution') or None
            slab.employer_min_amount = request.POST.get('employer_min_amount') or None

            slab.save()  # Save the updated slab
            messages.success(request, "Slab updated successfully!")
            return redirect('slab_master_index')
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    # Handle GET request to pre-fill form
    context = {
        'slab': slab,
        'slab_type': parameter_master.objects.filter(parameter_name='slab_type'),
        'slab_for': parameter_master.objects.filter(parameter_name='slab_for'),
        'applicable_designation': parameter_master.objects.filter(parameter_name='LWF type'),
        'slab_applicable': parameter_master.objects.filter(parameter_name='slab_applicable'),
    }
    return render(request, 'Tax/Slab/edit.html', context)


def slab_view(request, pk):
    act = request.GET.get('act')
    pk = decrypt_parameter(pk)
    slab = get_object_or_404(Slab, pk=pk)
    return render(request, 'Tax/Slab/view.html', {'slab': slab,'act':act})

def slab_master_index(request):
    try:
        # Fetching slabs with the related models using select_related for optimization
        slabs = SlabMaster.objects.select_related('state', 'city', 'act_id').all()
        
        # Encrypting pk if needed
        for slab in slabs:
            slab.pk = encrypt_parameter(str(slab.slab_id))
        
        return render(request, 'Tax/SlabMaster/index.html', {'slabs': slabs})
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)


def slab_master_create(request):
    months = [month for month in month_name if month]  # Generate month names, excluding the first empty string
    month_mapping = {month: i + 1 for i, month in enumerate(months)}  # Map month names to numbers

    if request.method == 'POST':
        form = SlabMasterForm(request.POST)
        try:
            if form.is_valid():
                try:
                    slab = form.save(commit=False)  
                    slab.slab_year = form.cleaned_data['slab_year'] 
                    slab.act_id = form.cleaned_data['act_id'] 
                    slab.period = form.cleaned_data['period']
                    slab.state = form.cleaned_data['state']
                    slab.city = form.cleaned_data.get('city')  
                    slab.slab_freq = form.cleaned_data['slab_freq']
                    slab.is_slab = form.cleaned_data['is_slab']
                    slab_months = request.POST.getlist('slab_months')  
                    slab.slab_months = ",".join(str(month_mapping[month]) for month in slab_months)
                    exception_months = request.POST.getlist('exception_month')
                    if exception_months:
                        slab.exception_month = ",".join(str(month_mapping[month]) for month in exception_months)
                    else:
                        slab.exception_month = None
                    slab.slab_status = form.cleaned_data['slab_status']
                    slab.created_by = request.user
                    slab.save()
                    messages.success(request, "Slab created successfully!")
                    return redirect('slab_master_index')

                except Exception as e:
                    return JsonResponse({'message': str(e)}, status=500)
            else:
                print(form.errors)
                messages.error(request, "Error creating Slab.")
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    else:
        form = SlabMasterForm()  # Instantiate an empty form for GET requests

    return render(request, 'Tax/SlabMaster/create.html', {'form': form, 'months': months})


# def slab_master_edit(request, pk):
#     # Decrypt the primary key and get the SlabMaster object
#     pk = decrypt_parameter(pk)
#     slab = get_object_or_404(SlabMaster, pk=pk)  # Fetch the SlabMaster object using the primary key
#     months = [month for month in month_name if month]  # Generate month names, excluding the first empty string
#     month_mapping = {month: i + 1 for i, month in enumerate(months)}  # Map month names to numbers

#     # Get the slab_months and exception_months from the slab object
#     slab_months = slab.slab_months.split(",") if slab.slab_months else []
#     exception_months = slab.exception_month.split(",") if slab.exception_month else []

#     if request.method == 'POST':
#         form = SlabMasterForm(request.POST, instance=slab)  # Pass the existing instance to the form
#         try:
#             if form.is_valid():
#                 # Save the form but don't commit yet
#                 slab = form.save(commit=False)

#                 # Update the fields with the cleaned data from the form
#                 slab.slab_year = form.cleaned_data['slab_year']
#                 slab.act_id = form.cleaned_data['act_id']
#                 slab.period = form.cleaned_data['period']
#                 slab.state = form.cleaned_data['state']
#                 slab.city = form.cleaned_data.get('city')  # Get city, if available
#                 slab.slab_freq = form.cleaned_data['slab_freq']
#                 slab.is_slab = form.cleaned_data['is_slab']
#                 slab.slab_status = form.cleaned_data['slab_status']
#                 slab.updated_by = request.user  # Update the updated_by field

#                 # Process the months and exception months
#                 slab_months = request.POST.getlist('slab_months')
#                 slab.slab_months = ",".join(str(month_mapping[month]) for month in slab_months)
                
#                 exception_months = request.POST.getlist('exception_month')
#                 if exception_months:
#                     slab.exception_months = ",".join(str(month_mapping[month]) for month in exception_months)
#                 else:
#                     slab.exception_months = None

#                 # Save the updated slab instance
#                 slab.save()
#                 messages.success(request, "Slab updated successfully!")
#                 return redirect('slab_master_index')

#             else:
#                 # Handle form errors
#                 messages.error(request, "Error updating Slab.")
#         except Exception as e:
#             return JsonResponse({'message': str(e)}, status=500)
#     else:
#         form = SlabMasterForm(instance=slab)

#     return render(request, 'Tax/SlabMaster/edit.html', {
#         'form': form,
#         'id': slab.slab_id,
#         'city_id': slab.city,
#         'months': months,
#         'slab_months': slab_months,
#         'exception_months': exception_months,
#     })

# Map numbers to month names


def slab_master_edit(request, pk):
    month_names = [
    "", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
    ]
    months = [month for month in month_name if month]  # Generate month names, excluding the first empty string
    month_mapping = {month: i + 1 for i, month in enumerate(months)}
    # Decrypt the primary key and get the SlabMaster object
    pk = decrypt_parameter(pk)
    slab = get_object_or_404(SlabMaster, pk=pk)  # Fetch the SlabMaster object using the primary key

    # Split the month strings into lists based on the numeric values
    slab_months = slab.slab_months.split(",") if slab.slab_months else []
    exception_months = slab.exception_month.split(",") if slab.exception_month else []

    # Convert numeric values to month names
    slab_months = [month_names[int(month)] for month in slab_months if month]
    exception_months = [month_names[int(month)] for month in exception_months if month]

    months = month_names[1:]  # List of month names (excluding the first empty string)

    if request.method == 'POST':
        form = SlabMasterForm(request.POST, instance=slab)  # Pass the existing instance to the form
        try:
            if form.is_valid():
                # Save the form but don't commit yet
                slab = form.save(commit=False)

                # Update the fields with the cleaned data from the form
                slab.slab_year = form.cleaned_data['slab_year']
                slab.act_id = form.cleaned_data['act_id']
                slab.period = form.cleaned_data['period']
                slab.state = form.cleaned_data['state']
                slab.city = form.cleaned_data.get('city')  # Get city, if available
                slab.slab_freq = form.cleaned_data['slab_freq']
                slab.is_slab = form.cleaned_data['is_slab']
                slab.slab_status = form.cleaned_data['slab_status']
                slab.updated_by = request.user  # Update the updated_by field

                # Process the months and exception months
                slab_months = request.POST.getlist('slab_months')
                slab.slab_months = ",".join(str(month_mapping[month]) for month in slab_months)
                
                exception_months = request.POST.getlist('exception_month')
                if exception_months:
                    slab.exception_month = ",".join(str(month_mapping[month]) for month in exception_months)
                else:
                    slab.exception_month = None

                # Save the updated slab instance
                slab.save()
                messages.success(request, "Slab updated successfully!")
                return redirect('slab_master_index')

            else:
                # Handle form errors
                messages.error(request, "Error updating Slab.")
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    else:
        form = SlabMasterForm(instance=slab)

    return render(request, 'Tax/SlabMaster/edit.html', {
        'form': form,
        'id': slab.slab_id,
        'city_id': slab.city,
        'months': months,
        'slab_months': slab_months,
        'exception_months': exception_months,
    })




def slab_master_view(request, pk):
    pk = decrypt_parameter(pk)
    slab = get_object_or_404(SlabMaster, pk=pk)
    return render(request, 'Tax/SlabMaster/view.html', {'slab': slab})


