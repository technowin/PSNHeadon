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
from Payroll.models import IncomeTaxMaster, payment_details as pay
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
            state.city_count = CityMaster.objects.filter(state_id=state.state_id).count()
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

# def slab_master_index(request):
#     try:
#         # Fetching slabs with the related models using select_related for optimization
#         slabs = SlabMaster.objects.all()
        
#         # Encrypting pk if needed
#         for slab in slabs:
#             slab.pk = encrypt_parameter(str(slab.slab_id))
        
#         return render(request, 'Tax/SlabMaster/index.html', {'slabs': slabs})
#     except Exception as e:
#         return JsonResponse({'message': str(e)}, status=500)

def slab_master_index(request):
    try:
        # Fetching slabs with the related models using select_related for optimization
        slabs = SlabMaster.objects.all()
        
        # Adding the count for employee and employer slabs
        for slab in slabs:
            # slab.pk = encrypt_parameter(str(slab.slab_id))
            employee_slab_count = Slab.objects.filter(slab_id=slab.slab_id, slab_type='Employee').count()
            employer_slab_count = Slab.objects.filter(slab_id=slab.slab_id, slab_type='Employer').count()
            slab.employee_slab_count = employee_slab_count
            slab.employer_slab_count = employer_slab_count
            slab.pk = encrypt_parameter(str(slab.slab_id))
        
        return render(request, 'Tax/SlabMaster/index.html', {'slabs': slabs})
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)


# def slab_master_create(request):
#     months = [month for month in month_name if month]  # Generate month names, excluding the first empty string
#     month_mapping = {month: i + 1 for i, month in enumerate(months)}  # Map month names to numbers

#     if request.method == 'POST':
#         form = SlabMasterForm(request.POST)
#         try:
#             if form.is_valid():
#                 try:
#                     slab = form.save(commit=False)  
#                     slab.slab_year = form.cleaned_data['slab_year'] 
#                     slab.act_id = form.cleaned_data['act_id'] 
#                     slab.period = form.cleaned_data['period']
#                     slab.state = form.cleaned_data['state']
#                     slab.city = form.cleaned_data.get('city')  
#                     slab.slab_freq = form.cleaned_data['slab_freq']
#                     slab.is_slab = form.cleaned_data['is_slab']
#                     slab_months = request.POST.getlist('slab_months')  
#                     slab.slab_months = ",".join(str(month_mapping[month]) for month in slab_months)
#                     exception_months = request.POST.getlist('exception_month')
#                     if exception_months:
#                         slab.exception_month = ",".join(str(month_mapping[month]) for month in exception_months)
#                     else:
#                         slab.exception_month = None
#                     slab.slab_status = form.cleaned_data['slab_status']
#                     slab.created_by = request.user
#                     slab.save()
#                     messages.success(request, "Slab created successfully!")
#                     return redirect('slab_master_index')

#                 except Exception as e:
#                     return JsonResponse({'message': str(e)}, status=500)
#             else:
#                 print(form.errors)
#                 messages.error(request, "Error creating Slab.")
#         except Exception as e:
#             return JsonResponse({'message': str(e)}, status=500)
#     else:
#         form = SlabMasterForm()  # Instantiate an empty form for GET requests

#     return render(request, 'Tax/SlabMaster/create.html', {'form': form, 'months': months})



def slab_master_create(request):

    months = [month for month in month_name if month] 
    month_mapping = {month: i + 1 for i, month in enumerate(months)}
    if request.method == 'POST':
        form = SlabMasterForm(request.POST)
        try:
            if form.is_valid():
                slab_year = form.cleaned_data['slab_year']
                act_id = form.cleaned_data['act_id']
                state = form.cleaned_data['state']
                city = form.cleaned_data.get('city')
                slab_freq = form.cleaned_data['slab_freq'].parameter_value

                # Check if record already exists
                existing_record = SlabMaster.objects.filter(
                    Q(act_id=act_id) & Q(state=state) & Q(city=city) & Q(slab_year=slab_year)
                ).exists()

                if existing_record:
                    messages.error(request, "A slab for the given criteria already exists.")
                    return redirect('slab_master_index')
                
                slab_months1 = request.POST.getlist("slab_months")
                slab_months1_nums = sorted(
                    [int(month_mapping[month]) for month in slab_months1]
                )
                def get_previous_months(start_month, num_months=6):
                    result = []
                    for i in range(num_months):
                        month = (start_month - i - 1) % 12
                        if month == 0:
                            month = 12
                        result.append(str(month))
                    return result[::-1]  # Return in ascending order

                def get_previous_months_quarterly(start_month, num_months=3):
                    result = []
                    for i in range(num_months):
                        month = (start_month - i - 1) % 12
                        if month == 0:
                            month = 12
                        result.append(str(month))
                    return result[::-1]

                def get_previous_months_yearly(start_month, num_months=12):
                    result = []
                    for i in range(num_months):
                        month = (start_month - i - 1) % 12
                        if month == 0:
                            month = 12
                        result.append(str(month))
                    return result[::-1]  # Return in ascending order

                def format_half_yearly(months):
                    if len(months) == 2:
                        month_ranges = []
                        for month in months:
                            month_range = get_previous_months(month, num_months=5) + [
                                str(month)
                            ]
                            month_ranges.append(",".join(month_range))
                        return " - ".join(month_ranges)
                    return " - ".join(
                        [
                            ",".join(map(str, slab_months1_nums[i : i + 6]))
                            for i in range(0, len(slab_months1_nums), 6)
                        ]
                    )

                def format_quarterly(months):
                    if len(months) == 4:
                        month_ranges = []
                        for month in months:
                            quarter_range = get_previous_months_quarterly(
                                month, num_months=2
                            ) + [str(month)]
                            month_ranges.append(",".join(quarter_range))
                        return " - ".join(month_ranges)
                    return ",".join(map(str, months))

                def format_yearly(months):
                    if len(months) == 1:
                        year_ranges = []
                        for month in months:
                            year_range = get_previous_months_yearly(
                                month, num_months=11
                            ) + [str(month)]
                            year_ranges.append(",".join(year_range))
                        return " - ".join(year_ranges)
                    return ",".join(map(str, months))

                slab_months1 = request.POST.getlist("slab_months")
                slab_months1_nums = sorted(
                    [int(month_mapping[month]) for month in slab_months1]
                )


                if slab_freq == "Half Yearly":
                    slab_months_challan_str = format_half_yearly(slab_months1_nums)
                elif slab_freq == "Quarterly":
                    slab_months_challan_str = format_quarterly(slab_months1_nums)
                elif slab_freq == "Yearly":
                    slab_months_challan_str = format_yearly(slab_months1_nums)
                else:
                    slab_months_challan_str = ",".join(map(str, slab_months1_nums))


                slab_months_str = ",".join(map(str, slab_months1_nums))


                # Create the slab instance
                slab = form.save(commit=False)
                slab.slab_year = slab_year
                slab.act_id = act_id
                slab.period = form.cleaned_data['period']
                slab.state = state
                slab.city = city
                slab.slab_freq = slab_freq
                slab.is_slab = form.cleaned_data['is_slab']
                slab.slab_months = slab_months_str
                slab.slab_months_challan = slab_months_challan_str

                exception_months = request.POST.getlist('exception_month')
                if exception_months:
                    slab.exception_month = ",".join(
                        str(month_mapping[month]) for month in exception_months
                    )
                else:
                    slab.exception_month = None

                slab.slab_status = form.cleaned_data['slab_status']
                slab.created_by = request.user

                slab.save()
                messages.success(request, "Slab created successfully!")
                return redirect('slab_master_index')

            else:
                print(form.errors)
                messages.error(request, "Error creating Slab.")
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    else:
        form = SlabMasterForm()  # Instantiate an empty form for GET requests

    return render(request, 'Tax/SlabMaster/create.html', {'form': form, 'months': months})



def slab_master_edit(request, pk):
    month_names = [
    "", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
    ]
    months = [month for month in month_name if month]  
    month_mapping = {month: i + 1 for i, month in enumerate(months)}
    
    pk = decrypt_parameter(pk)
    slab = get_object_or_404(SlabMaster, pk=pk)  
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
                slab_year = form.cleaned_data['slab_year'].year
                act_id = form.cleaned_data['act_id']
                state = form.cleaned_data['state']
                city = form.cleaned_data.get('city')
                slab_freq = form.cleaned_data['slab_freq'].parameter_value
                period = form.cleaned_data['period'].parameter_value

                
                slab_months1 = request.POST.getlist("slab_months")
                slab_months1_nums = sorted(
                    [int(month_mapping[month]) for month in slab_months1]
                )
                def get_previous_months(start_month, num_months=6):
                    result = []
                    for i in range(num_months):
                        month = (start_month - i - 1) % 12
                        if month == 0:
                            month = 12
                        result.append(str(month))
                    return result[::-1]  # Return in ascending order

                def get_previous_months_quarterly(start_month, num_months=3):
                    result = []
                    for i in range(num_months):
                        month = (start_month - i - 1) % 12
                        if month == 0:
                            month = 12
                        result.append(str(month))
                    return result[::-1]

                def get_previous_months_yearly(start_month, num_months=12):
                    result = []
                    for i in range(num_months):
                        month = (start_month - i - 1) % 12
                        if month == 0:
                            month = 12
                        result.append(str(month))
                    return result[::-1]  # Return in ascending order

                def format_half_yearly(months):
                    if len(months) == 2:
                        month_ranges = []
                        for month in months:
                            month_range = get_previous_months(month, num_months=5) + [
                                str(month)
                            ]
                            month_ranges.append(",".join(month_range))
                        return " - ".join(month_ranges)
                    return " - ".join(
                        [
                            ",".join(map(str, slab_months1_nums[i : i + 6]))
                            for i in range(0, len(slab_months1_nums), 6)
                        ]
                    )

                def format_quarterly(months):
                    if len(months) == 4:
                        month_ranges = []
                        for month in months:
                            quarter_range = get_previous_months_quarterly(
                                month, num_months=2
                            ) + [str(month)]
                            month_ranges.append(",".join(quarter_range))
                        return " - ".join(month_ranges)
                    return ",".join(map(str, months))

                def format_yearly(months):
                    if len(months) == 1:
                        year_ranges = []
                        for month in months:
                            year_range = get_previous_months_yearly(
                                month, num_months=11
                            ) + [str(month)]
                            year_ranges.append(",".join(year_range))
                        return " - ".join(year_ranges)
                    return ",".join(map(str, months))

                slab_months1 = request.POST.getlist("slab_months")
                slab_months1_nums = sorted(
                    [int(month_mapping[month]) for month in slab_months1]
                )


                if slab_freq == "Half Yearly":
                    slab_months_challan_str = format_half_yearly(slab_months1_nums)
                elif slab_freq == "Quarterly":
                    slab_months_challan_str = format_quarterly(slab_months1_nums)
                elif slab_freq == "Yearly":
                    slab_months_challan_str = format_yearly(slab_months1_nums)
                else:
                    slab_months_challan_str = ",".join(map(str, slab_months1_nums))


                slab_months_str = ",".join(map(str, slab_months1_nums))
                
                slab = form.save(commit=False)
                slab.slab_year = slab_year
                slab.act_id = act_id
                slab.period = period
                slab.state = state
                slab.city = city
                slab.slab_freq = slab_freq
                slab.is_slab = form.cleaned_data['is_slab']
                slab.slab_months = slab_months_str
                slab.slab_months_challan = slab_months_challan_str

                exception_months = request.POST.getlist('exception_month')
                if exception_months:
                    slab.exception_month = ",".join(
                        str(month_mapping[month]) for month in exception_months
                    )
                else:
                    slab.exception_month = None

                slab.slab_status = form.cleaned_data['slab_status']
                slab.created_by = request.user

                slab.save()
                messages.success(request, "Slab Updated successfully!")
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




# def slab_master_view(request, pk):
#     pk = decrypt_parameter(pk)
#     slab = get_object_or_404(SlabMaster, pk=pk)
#     return render(request, 'Tax/SlabMaster/view.html', {'slab': slab})
def slab_master_view(request, pk):
    pk = decrypt_parameter(pk)
    slab = get_object_or_404(SlabMaster, pk=pk)
    
    # Mapping month numbers (1-12) to month names (January - December)
    month_mapping = {i: month for i, month in enumerate(month_name[1:], start=1)}

    # Debugging: Check the data type and contents of slab_months
    print(f"slab_months: {slab.slab_months}")
    print(f"Type of slab_months: {type(slab.slab_months)}")
    
    # Ensure slab_months is a list of integers
    if isinstance(slab.slab_months, list):
        slab_months = slab.slab_months  # If it's already a list
    elif isinstance(slab.slab_months, str):
        # If it's a comma-separated string, convert it to a list of integers
        slab_months = [int(month) for month in slab.slab_months.split(',')]
    else:
        # Handle other cases like a queryset or other types
        slab_months = list(slab.slab_months.values_list('month_field', flat=True))
    
    # Convert the month numbers into month names
    slab_month_names = [month_mapping[month] for month in slab_months]


    if slab.exception_month is None or not slab.exception_month:
        exception_month_names = None  # No exception months, set to None
    else:
        # Process exception_month if it is provided
        if isinstance(slab.exception_month, list):
            exception_month = slab.exception_month  # If it's already a list
        elif isinstance(slab.exception_month, str):
            exception_month = [int(month) for month in slab.exception_month.split(',')]  # Convert comma-separated string
        else:
            exception_month = list(slab.exception_month.values_list('month_field', flat=True))  # Handle other cases

        # Convert exception month numbers into month names
        exception_month_names = [month_mapping[month] for month in exception_month]
    
    # Pass the data to the template
    return render(request, 'Tax/SlabMaster/view.html', {
        'slab': slab,
        'slab_month_names': slab_month_names,
        'exception_month_names':exception_month_names
    })

    


def check_slab_combination(request):
    if request.method == 'POST':
        state_id = request.POST.get('state_id')
        city_id = request.POST.get('city_id') or None
        act_id = request.POST.get('act_id')
        slab_freq = request.POST.get('slab_freq')

        # Query to check if the combination exists
        exists = SlabMaster.objects.filter(state=state_id, city=city_id, act_id=act_id, slab_freq=slab_freq).exists()

    return JsonResponse({'exists': exists})


def income_tax_master_index(request):
    try:
        incomeTax = IncomeTaxMaster.objects.all()
        for income in incomeTax:
            income.pk = encrypt_parameter(str(income.id))  # Add encrypted ID dynamically
        
        return render(request, 'Tax/IncomeTax/index.html', {'incomeTax': incomeTax})  # Pass incomeTax
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)



    
def income_tax_create(request):
    if request.method == 'POST':
        form = IncomeTaxMasterForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)  # Don't save to the database yet
            income.created_by = request.user   # Also set updated_by initially
            income.save()  # Now save to the database
            messages.success(request, "Income Slab created successfully!")
            return redirect('income_tax_master_index')
        else:
            messages.error(request, "Error creating Salary Element.")
    else:
        form = IncomeTaxMasterForm()
    return render(request, 'Tax/IncomeTax/create.html', {'form': form})

def income_tax_edit(request, pk):
    pk = decrypt_parameter(pk)
    id = get_object_or_404(IncomeTaxMaster, pk=pk)

    if request.method == 'POST':
        form = IncomeTaxMasterForm(request.POST, instance=id)
        if form.is_valid():
            income = form.save(commit=False)  # Don't save to the database yet
            income.updated_by = request.user  # Also set updated_by initially
            income.save()  # Now save to the database
            messages.success(request, "Income slab Updated successfully!")
            return redirect('income_tax_master_index')
        else:
            messages.error(request, "Error updating Salary Element.")
    else:
        form = IncomeTaxMasterForm(instance=id)
    
    return render(request, 'Tax/IncomeTax/edit.html', {'form': form, 'id': id})

def income_tax_view(request, pk):
    pk = decrypt_parameter(pk)
    income = get_object_or_404(IncomeTaxMaster, pk=pk)
    return render(request, 'Tax/IncomeTax/view.html', {'income': income})




