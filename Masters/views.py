import json
import pydoc
from django.contrib import messages
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate, login ,logout,get_user_model
from grpc import Status
from Account.forms import RegistrationForm
from Account.models import *
from Masters.models import *
from datetime import date
from Masters.models import site_master as sit
from Masters.models import SlotDetails as slot
from Masters.models import company_master as com
from Payroll.models import * 
import Db 
import re
from datetime import datetime


import bcrypt
from django.contrib.auth.decorators import login_required
from Masters.serializers import ScRosterSerializer,EmployeeSerializer, SettingMasterSerializer, SlotDetailsSerializer, SlotListDetailsSerializer, StateMasterSerializer, UserSlotDetailsSerializer, UserSlotlistSerializer
from Notification.models import notification_log
from Notification.serializers import NotificationSerializer
from PSNHeadon.encryption import *
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from Account.utils import decrypt_email, encrypt_email
import requests
import traceback
import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib import messages
import openpyxl
from openpyxl.styles import Font, Border, Side
import calendar
from datetime import datetime, timedelta
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from django.utils import timezone
from .models import Log, sc_roster, sc_employee_master, CustomUser 
from django.shortcuts import render
from django.db import connection

@login_required
def masters(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    pre_url = request.META.get('HTTP_REFERER')
    header, data = [], []
    entity, type, name = '', '', ''
    global user
    user  = request.session.get('user_id', '')
    try:
         
        if request.method=="GET":
            entity = request.GET.get('entity', '')
            type = request.GET.get('type', '')
            cursor.callproc("stp_get_masters",[entity,type,'name',user])
            for result in cursor.stored_results():
                datalist1 = list(result.fetchall())
            name = datalist1[0][0]
            cursor.callproc("stp_get_masters", [entity, type, 'header',user])
            for result in cursor.stored_results():
                header = list(result.fetchall())
            cursor.callproc("stp_get_masters",[entity,type,'data',user])
            for result in cursor.stored_results():
                if (entity == 'em' or entity == 'sm' or entity == 'cm' or entity == 'menu' or entity == 'user' or entity =='sd' or entity =='dm' or entity =='um') and type !='err': 
                    data = []
                    rows = result.fetchall()
                    for row in rows:
                        encrypted_id = encrypt_parameter(str(row[0]))
                        data.append((encrypted_id,) + row[1:])
                else: data = list(result.fetchall())

            cursor.callproc("stp_get_dropdown_values",['company'])
            for result in cursor.stored_results():
                company_names = list(result.fetchall())
            cursor.callproc("stp_get_dropdown_values",['site'])
            for result in cursor.stored_results():
                site_name = list(result.fetchall())
            cursor.callproc("stp_get_dropdown_values",['designation'])
            for result in cursor.stored_results():
                designation_name = list(result.fetchall())
            
            if entity == 'r' and type == 'i':
                cursor.callproc("stp_get_assigned_company",[user])
                for result in cursor.stored_results():
                    company_names = list(result.fetchall())
            if entity == 'r' and type == 'ed':
                month_year =str(request.GET.get('month', ''))
                if month_year == '':
                    year,month = '',''
                else: year,month = month_year.split('-')
                employee_id = request.GET.get('empid', '')
                cursor.callproc("stp_get_edit_roster",[employee_id,month,year,'1'])
                for result in cursor.stored_results():
                    data = list(result.fetchall())
                cursor.callproc("stp_get_edit_roster",[employee_id,month,year,'2'])
                for result in cursor.stored_results():
                    header = list(result.fetchall())
            if entity == 'urm' and (type == 'acu' or type == 'acr'):
                cursor.callproc("stp_get_access_control",[entity,type])
                for result in cursor.stored_results():
                    header = list(result.fetchall())
                cursor.callproc("stp_get_access_control",[entity,'comp'])
                for result in cursor.stored_results():
                    company_names = list(result.fetchall())
                cursor.callproc("stp_get_access_control",[entity,'site'])
                for result in cursor.stored_results():
                    data = list(result.fetchall())
                
        if request.method=="POST":
            entity = request.POST.get('entity', '')
            type = request.POST.get('type', '')
            if entity == 'r' and type == 'ed':
                ids = request.POST.getlist('ids[]', '')
                shifts = request.POST.getlist('shifts[]', '')
                for id,shift in zip(ids, shifts):
                    cursor.callproc("stp_post_roster",[id,shift])
                    for result in cursor.stored_results():
                        datalist = list(result.fetchall())
                if datalist[0][0] == "success":
                    messages.success(request, 'Data updated successfully !')
            if entity == 'urm' and (type == 'acu' or type == 'acr'):
                
                created_by = request.session.get('user_id', '')
                ur = request.POST.get('ur', '')
                selected_company_ids = list(map(int, request.POST.getlist('company_id')))
                selected_worksites  = request.POST.getlist('worksite')
                company_worksite_map = {}
                
                if not selected_company_ids or not selected_worksites:
                    messages.error(request, 'Company or worksite data is missing!')
                    return redirect(f'/masters?entity={entity}&type=urm')
                if type not in ['acu', 'acr'] or not ur:
                    messages.error(request, 'Invalid data received.')
                    return redirect(f'/masters?entity={entity}&type=urm')
                
                cursor.callproc("stp_get_company_worksite",[",".join(request.POST.getlist('company_id'))])
                for result in cursor.stored_results():
                    company_worksites  = list(result.fetchall())
                    
                for company_id, worksite_name in company_worksites:
                    if company_id not in company_worksite_map:
                        company_worksite_map[company_id] = []
                    company_worksite_map[company_id].append(worksite_name)
                
                filtered_combinations = []
                for company_id in selected_company_ids:
                    valid_worksites = company_worksite_map.get(company_id, [])
                    # Filter worksites that were actually selected by the user
                    selected_valid_worksites = [ws for ws in selected_worksites if ws in valid_worksites]
                    filtered_combinations.extend([(company_id, ws) for ws in selected_valid_worksites])
                    
                cursor.callproc("stp_delete_access_control",[type,ur])
                r=''
                for company_id, worksite in filtered_combinations:
                    cursor.callproc("stp_post_access_control",[type,ur,company_id,worksite,created_by])
                    for result in cursor.stored_results():
                            r = list(result.fetchall())
                type='urm'
                if r[0][0] == "success":
                    messages.success(request, 'Data updated successfully !')
                
            else : messages.error(request, 'Oops...! Something went wrong!')
                             
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        cursor.callproc("stp_error_log",[fun,str(e),user])  
        messages.error(request, 'Oops...! Something went wrong!')
    finally:
        cursor.close()
        m.commit()
        m.close()
        Db.closeConnection()
        if request.method=="GET":
            return render(request,'Master/index.html', {'entity':entity,'type':type,'name':name,'header':header,'company_names':company_names,'site_name':site_name,'designation_name':designation_name,'data':data,'pre_url':pre_url})
        elif request.method=="POST":  
            new_url = f'/masters?entity={entity}&type={type}'
            return redirect(new_url) 
        
def gen_roster_xlsx_col(columns,month_input):
    year, month = map(int, month_input.split('-'))
    _, num_days = calendar.monthrange(year, month)
    date_columns = [(datetime(year, month, day)).strftime('%d-%m-%Y') for day in range(1, num_days + 1)]
    columns.extend(date_columns)
    return columns

def sample_xlsx(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor = m.cursor()
    pre_url = request.META.get('HTTP_REFERER')
    response = ''
    global user
    user = request.session.get('user_id', '')

    try:
        # Create a new workbook
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Sample Format'
        columns = []

        # Fetching entity and type based on request method
        if request.method == "GET":
            entity = request.GET.get('entity', '')  # Ensure entity is fetched from GET
            type = request.GET.get('type', '')
        elif request.method == "POST":
            entity = request.POST.get('entity', '')  # Ensure entity is fetched from POST
            type = request.POST.get('type', '')

        # Map the entity to a file name
        file_name = {
            'em': 'Employee Master',
            'sm': 'Worksite Master',
            'cm': 'Company Master',
            'r': 'Roster',
            'um': 'Employee Master Upload'
        }.get(entity, 'Unknown File')

        # Call stored procedure with provided parameters
        cursor.callproc("stp_get_masters", [entity, type, 'sample_xlsx', user])

        for result in cursor.stored_results():
            columns = [col[0] for col in result.fetchall()]

        # Additional logic for roster entity
        if entity == "r":
            month = request.POST.get('month', '')
            columns = gen_roster_xlsx_col(columns, month)

        # Define black border style
        black_border = Border(
            left=Side(border_style="thin", color="000000"),
            right=Side(border_style="thin", color="000000"),
            top=Side(border_style="thin", color="000000"),
            bottom=Side(border_style="thin", color="000000")
        )

        # Write headers to the Excel file
        for col_num, header in enumerate(columns, 1):
            cell = sheet.cell(row=1, column=col_num)
            cell.value = header
            cell.font = Font(bold=True)
            cell.border = black_border

        # Adjust column widths
        for col in sheet.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            adjusted_width = max_length + 2
            sheet.column_dimensions[column].width = adjusted_width

        # Create HTTP response with Excel file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="{} {}.xlsx"'.format(file_name, datetime.now().strftime("%d-%m-%Y"))
        workbook.save(response)

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        cursor.callproc("stp_error_log", [fun, str(e), user])
        messages.error(request, 'Oops...! Something went wrong!')

    finally:
        cursor.close()
        m.commit()
        m.close()
        Db.closeConnection()

    return response
        
# def sample_xlsx(request):
#     Db.closeConnection()
#     m = Db.get_connection()
#     cursor=m.cursor()
#     pre_url = request.META.get('HTTP_REFERER')
#     response =''
#     global user
#     user  = request.session.get('user_id', '')
#     try:
        
#         workbook = openpyxl.Workbook()
#         sheet = workbook.active
#         sheet.title = 'Sample Format'
#         columns = []
#         if request.method=="GET":
#             entity = request.GET.get('entity', '')
#             type = request.GET.get('type', '')
#         if request.method=="POST":
#             entity = request.POST.get('entity', '')
#             type = request.POST.get('type', '')
#         file_name = {'em': 'Employee Master','sm': 'Worksite Master','cm': 'Company Master','r': 'Roster','um': 'Employee Master Upload'}[entity]
#         cursor.callproc("stp_get_masters", [entity, type, 'sample_xlsx',user])
#         for result in cursor.stored_results():
#             columns = [col[0] for col in result.fetchall()]
#         # columns = ['Column 1', 'Column 2', 'Column 3']
#         if entity == "r":
#             month = request.POST.get('month', '')
#             columns = gen_roster_xlsx_col(columns,month)

#         black_border = Border(
#             left=Side(border_style="thin", color="000000"),
#             right=Side(border_style="thin", color="000000"),
#             top=Side(border_style="thin", color="000000"),
#             bottom=Side(border_style="thin", color="000000")
#         )
        
#         for col_num, header in enumerate(columns, 1):
#             cell = sheet.cell(row=1, column=col_num)
#             cell.value = header
#             cell.font = Font(bold=True)
#             cell.border = black_border
        
#         for col in sheet.columns:
#             max_length = 0
#             column = col[0].column_letter  
#             for cell in col:
#                 if len(str(cell.value)) > max_length:
#                     max_length = len(str(cell.value))
                    
#             adjusted_width = max_length + 2 
#             sheet.column_dimensions[column].width = adjusted_width  
#         response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#         response['Content-Disposition'] = 'attachment; filename="' + str(file_name) +" "+str(datetime.now().strftime("%d-%m-%Y")) + '.xlsx"'
#         workbook.save(response)
    
#     except Exception as e:
#         tb = traceback.extract_tb(e.__traceback__)
#         fun = tb[0].name
#         cursor.callproc("stp_error_log",[fun,str(e),user])  
#         messages.error(request, 'Oops...! Something went wrong!')
#     finally:
#         cursor.close()
#         m.commit()
#         m.close()
#         Db.closeConnection()
#         return response      

@login_required  
def roster_upload(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor = m.cursor()
    global user
    user  = request.session.get('user_id', '')
    if request.method == 'POST' and request.FILES.get('roster_file'):
        try:
            excel_file = request.FILES['roster_file']
            file_name = excel_file.name
            df = pd.read_excel(excel_file)

            entity = request.POST.get('entity', '')
            type = request.POST.get('type', '')
            company_id = request.POST.get('company_id', '')
            month_input  =str(request.POST.get('month_year', ''))
            total_rows = len(df)
            update_count = error_count = success_count = 0
            checksum_id = None
            worksites = []

            if entity == 'r':
                year, month = map(int, month_input.split('-'))
                _, num_days = calendar.monthrange(year, month)
                date_columns = [(datetime(year, month, day)).strftime('%d-%m-%Y') for day in range(1, num_days + 1)]
                cursor.callproc("stp_get_masters", [entity, type, 'sample_xlsx',user])
                for result in cursor.stored_results():
                    start_columns = [col[0] for col in result.fetchall()]

                if not all(col in df.columns for col in start_columns + date_columns):
                    messages.error(request, 'Oops...! The uploaded Excel file does not contain the required columns.!')
                    return redirect(f'/masters?entity={entity}&type={type}')
                
                cursor.callproc('stp_insert_checksum', ('roster',company_id,month,year,file_name))
                for result in cursor.stored_results():
                    c = list(result.fetchall())
                checksum_id = c[0][0]
                
                for index,row in df.iterrows():
                    employee_id = row.get('Employee Id', '')
                    employee_name = row.get('Employee Name', '')
                    worksite  = row.get('Worksite', '')
                    
                    for date_col in date_columns:
                        shift_date = datetime.strptime(date_col, '%d-%m-%Y').date()
                        shift_time = row.get(date_col) 
                        if pd.isna(shift_time):
                            shift_time = None
                        params = (str(employee_id),employee_name,int(company_id),worksite,shift_date,shift_time,checksum_id,user)
                        cursor.callproc('stp_insert_roster', params)
                        for result in cursor.stored_results():
                            r = list(result.fetchall())
                        if r[0][0] not in ("success", "updated"):
                            if worksite not in worksites:
                                worksites.append(worksite)
                            error_message = str(r[0][0])
                            error_params = ('roster', company_id,worksite,file_name,shift_date,error_message,checksum_id)
                            cursor.callproc('stp_insert_error_log', error_params)
                            messages.error(request, "Errors occurred during upload. Please check error logs.")
                    if r[0][0] == "success": success_count += 1
                    elif r[0][0] == "updated": update_count += 1  
                    else: error_count += 1
                checksum_msg = f"Total Rows Processed: {total_rows}, Successful Entries: {success_count}, Updates: {update_count}, Errors: {error_count}"
                cursor.callproc('stp_update_checksum', ('roster',company_id,', '.join(worksites),month,year,file_name,checksum_msg,error_count,update_count,checksum_id))
                if error_count == 0 and update_count == 0 and success_count > 0:
                    messages.success(request, f"All data uploaded successfully!.")
                elif error_count == 0 and success_count == 0 and update_count > 0:
                    messages.warning(request, f"All data updated successfully!.")
                else:
                    messages.warning(request, f"The upload processed {total_rows} rows, resulting in {success_count} successful entries, {update_count} updates, and {error_count} errors; please check the error logs for details.")
                    
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            fun = tb[0].name
            cursor.callproc("stp_error_log", [fun, str(e), user])  
            messages.error(request, 'Oops...! Something went wrong!')
            m.commit()   

        finally:
            cursor.close()
            m.close()
            Db.closeConnection()
            return redirect(f'/masters?entity={entity}&type={type}')     
        
@login_required        
def site_master(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    global user
    user  = request.session.get('user_id', '')
    try:
        
        if request.method == "GET":
            cursor.callproc("stp_get_roster_type")
            for result in cursor.stored_results():
                roster_types = list(result.fetchall())
                # Call stored procedure to get company names
            cursor.callproc("stp_get_company_names")
            for result in cursor.stored_results():
                company_names = list(result.fetchall())
            site_id = request.GET.get('site_id', '')
            if site_id == "0":
                if request.method == "GET":
                    context = {'company_names': company_names, 'roster_type': roster_types,'site_id':site_id}

            else:
                site_id1 = request.GET.get('site_id', '')
                site_id = decrypt_parameter(site_id1)
                cursor.callproc("stp_edit_site_master", (site_id,)) 
                for result in cursor.stored_results():
                    data = result.fetchall()[0]  
                    context = {
                        'roster_types':roster_types,
                        'company_names':company_names,
                        'site_id' : data[0],
                        'site_name': data[1],
                        'site_address': data[2],
                        'pincode': data[3],
                        'contact_person_name': data[4],
                        'contact_person_email': data[5], 
                        'contact_person_mobile_no': data[6],
                        'is_active':data[7],
                        'no_of_days': data[8],               
                        'notification_time': data[9],
                        'reminder_time': data[10],
                        'company_name' :data[11],
                        'roster_type': data[13]
                    }

        if request.method == "POST":
            siteId = request.POST.get('site_id', '')
            if siteId == "0":
                response_data = {"status": "fail"}
                
                siteName = request.POST.get('siteName', '')
                siteAddress = request.POST.get('siteAddress', '')
                pincode = request.POST.get('pincode', '')
                contactPersonName = request.POST.get('contactPersonName', '')
                contactPersonEmail = request.POST.get('contactPersonEmail', '')
                contactPersonMobileNo = request.POST.get('Number', '')  
                # is_active = request.POST.get('status_value', '') 
                # noOfDays = request.POST.get('FieldDays', '')  
                # notificationTime = request.POST.get('notificationTime', '')
                # ReminderTime = request.POST.get('ReminderTime', '')
                companyId = request.POST.get('company_id', '')  
                # rosterType = request.POST.get('roster_type', '')
               
                params = [
                    siteName, 
                    siteAddress, 
                    pincode, 
                    contactPersonName, 
                    contactPersonEmail, 
                    contactPersonMobileNo, 
                    # is_active,
                    # noOfDays, 
                    # notificationTime, 
                    # ReminderTime, 
                    companyId
                    # rosterType
                ]
                
                cursor.callproc("stp_insert_site_master", params)
                for result in cursor.stored_results():
                        datalist = list(result.fetchall())
                if datalist[0][0] == "success":
                    messages.success(request, 'Data successfully entered !')
                else: messages.error(request, datalist[0][0])
            else:
                if request.method == "POST" :
                    siteId = request.POST.get('site_id', '')
                    siteName = request.POST.get('siteName', '')
                    siteAddress = request.POST.get('siteAddress', '')
                    pincode = request.POST.get('pincode', '')
                    contactPersonName = request.POST.get('contactPersonName', '')
                    contactPersonEmail = request.POST.get('contactPersonEmail', '')
                    contactPersonMobileNo = request.POST.get('Number', '')  
                    # noOfDays = request.POST.get('FieldDays', '') 
                    isActive = request.POST.get('status_value', '')
                    # notificationTime = request.POST.get('notificationTime', '')
                    # ReminderTime = request.POST.get('ReminderTime', '')
                    CompanyId = request.POST.get('company_id', '')
                    # Rostertype = request.POST.get('roster_type', '')
                    
                    params = [siteId,siteName,siteAddress,pincode,contactPersonName,contactPersonEmail,
                                        contactPersonMobileNo,isActive,CompanyId]
                    cursor.callproc("stp_update_site_master",params) 
                    messages.success(request, "Data updated successfully...!")

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        cursor.callproc("stp_error_log", [fun, str(e), user])  
        messages.error(request, 'Oops...! Something went wrong!')
    finally:
        cursor.close()
        m.commit()
        m.close()
        Db.closeConnection()
            
        if request.method=="GET":
            return render(request, "Master/site_master.html", context)
        elif request.method=="POST":  
            return redirect( f'/masters?entity=sm&type=i')
        
@login_required      
def company_master(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    global user
    user  = request.session.get('user_id', '')
    try:
        
        if request.method == "GET":
        
            company_id = request.GET.get('company_id', '')
            if company_id == "0":
                if request.method == "GET":
                    context = {'company_id':company_id}
            else:
                company_id1 = request.GET.get('company_id', '')
                company_id= decrypt_parameter(company_id1)
                cursor.callproc("stp_edit_company_master", (company_id,))  # Note the comma to make it a tuple
                for result in cursor.stored_results():
                    data = result.fetchall()[0]  
                        
                    context = {
                        'company_id' : data[0],
                        'company_name': data[1],
                        'company_address': data[2],
                        'pincode': data[3],
                        'contact_person_name': data[4],
                        'contact_person_email': data[5], 
                        'contact_person_mobile_no': data[6],
                        'is_active':data[7]
                    }

        if request.method == "POST" :
            company_id = request.POST.get('company_id', '')
            if company_id == '0':
                response_data = {"status": "fail"}
                company_name = request.POST.get('company_name', '')
                company_address = request.POST.get('company_address', '')
                pincode = request.POST.get('pincode', '')
                contact_person_name = request.POST.get('contact_person_name', '')
                contact_person_email = request.POST.get('contact_person_email', '')
                contact_person_mobile_no = request.POST.get('contact_person_mobile_no', '') 
                # is_active = request.POST.get('status_value', '') 
                params = [
                    company_name, 
                    company_address, 
                    pincode, 
                    contact_person_name,
                    contact_person_email,
                    contact_person_mobile_no
                    # is_active
                ]
                cursor.callproc("stp_insert_company_master", params)
                for result in cursor.stored_results():
                        datalist = list(result.fetchall())
                if datalist[0][0] == "success":
                    messages.success(request, 'Data successfully entered !')
                else: messages.error(request, datalist[0][0])
            else :
                company_id = request.POST.get('company_id', '')
                company_name = request.POST.get('company_name', '')
                company_address = request.POST.get('company_address', '')
                pincode = request.POST.get('pincode', '')
                contact_person_name = request.POST.get('contact_person_name', '')
                contact_person_email = request.POST.get('contact_person_email', '')
                contact_person_mobile_no = request.POST.get('contact_person_mobile_no', '') 
                is_active = request.POST.get('status_value', '') 
                   
                params = [company_id,company_name,company_address,pincode,contact_person_name,contact_person_email,
                                            contact_person_mobile_no,is_active]    
                cursor.callproc("stp_update_company_master",params) 
                messages.success(request, "Data updated successfully ...!")
                
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        cursor.callproc("stp_error_log", [fun, str(e), user])  
        messages.error(request, 'Oops...! Something went wrong!')
    finally:
        cursor.close()
        m.commit()
        m.close()
        Db.closeConnection()

        encrypted_id = encrypt_parameter(company_id)
            
        if request.method=="GET":
            return render(request, "Master/company_master.html", context)
        elif request.method == "POST":
            return redirect(f'/masters?entity=cm&type=i')

@login_required        
def employee_master(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    global user
    
    # user_id = request.session.get('user_id', '')
    # user = CustomUser.objects.get(id=user_id)
    try:
        
        if request.method == "GET":
            id = request.GET.get('id', '')
            

            cursor.callproc("stp_get_employee_status")
            for result in cursor.stored_results():
                employee_status = list(result.fetchall())
            cursor.callproc("stp_get_dropdown_values",('site',))
            for result in cursor.stored_results():
                site_name = list(result.fetchall())
            cursor.callproc("stp_get_dropdown_values",('company',))
            for result in cursor.stored_results():
                company_names = list(result.fetchall())
            cursor.callproc("stp_get_dropdown_values",('states',))
            for result in cursor.stored_results():
                state_names = list(result.fetchall())
            cursor.callproc("stp_get_dropdown_values",('gender',))
            for result in cursor.stored_results():
                gender = list(result.fetchall())
            cursor.callproc("stp_get_dropdown_values",('designation',))
            for result in cursor.stored_results():
                designation_name = list(result.fetchall())
            if id == "0":
                if request.method == "GET":
                    context = {'id':id, 'employee_status':employee_status, 'employee_status_id': '','site_name':site_name,'gender':gender ,'company_names':company_names,'state_names':state_names,'designation_name':designation_name}

            else:
                id1 = request.GET.get('id', '')
                id = decrypt_parameter(id1)
                cursor.callproc("stp_edit_employee_master", (id,))
                for result in cursor.stored_results():
                    data = result.fetchall()[0]  
                    context = {
                        'id':id, 
                        'employee_status':employee_status, 
                        'site_name':site_name,
                        'designation_name':designation_name,
                        'gender':gender ,
                        'company_names':company_names,
                        'state_names':state_names,
                        'employee_status':employee_status,
                        'employee_id' : data[0],
                        'employee_name': data[1],
                        'mobile_no': data[2],
                        'email':data[3], 
                        'gender_value': data[4],
                        'state_id_value':data[5],
                        'city':data[6],
                        'address':data[7],
                        'pincode':data[8],
                        'account_holder_name':data[9],
                        'account_no':data[10],
                        'bank_name':data[11],
                        'branch_name':data[12],
                        'ifsc_code':data[13],
                        'pf_no':data[14],
                        'uan_no':data[15],
                        'esic':data[16],
                        'employment_status_id': data[17],
                        'handicapped_value': data[18],
                        'is_active': data[19],     
                        'company_id_value':data[20],
                    }
                    employee_id = context['employee_id']
                    designation_list = employee_designation.objects.filter(employee_id=employee_id)
                    context['selected_designation'] = json.dumps(list(map(str, designation_list.values_list('designation_id', flat=True)))) 


                    site_list = employee_site.objects.filter(employee_id=employee_id)
                    context['selected_site'] = json.dumps(list(map(str,site_list.values_list('site_id', flat=True)))) 




        if request.method == "POST" :
            id = request.POST.get('id', '')
            if id == '0':

                employeeId = request.POST.get('employee_id', '')
                employeeName = request.POST.get('employee_name', '')
                mobile_no = request.POST.get('mobile_no', '')
                email= request.POST.get('email', '')
                gender = request.POST.get('gender', '')
                handicapped = request.POST.get('handicapped_value', '')
                address = request.POST.get('address', '')
                city = request.POST.get('city', '')
                state1 = request.POST.get('state_id', '')
                pincode = request.POST.get('pincode', '')
                company_id1 = request.POST.get('company_id', '')
                account_holder_name = request.POST.get('account_holder_name', '')
                account_no = request.POST.get('account_no', '')
                bank_name = request.POST.get('bank_name', '')
                branch_name = request.POST.get('branch_name', '')
                ifsc_code = request.POST.get('ifsc_code', '')
                pf_no = request.POST.get('pf_no', '')
                uan_no = request.POST.get('uan_no', '')
                esic = request.POST.get('esic', '')
                # employeeStatus = request.POST.get('employee_status_id', '')
                # activebtn = request.POST.get('status_value', '')
                designation_list = request.POST.getlist('designation_name', '')
                site_list = request.POST.getlist('site_name', '')
                for designation in designation_list:
                    designation_id = designation_master.objects.get(designation_id=int(designation))
                    employee_designation.objects.create(employee_id=employeeId,designation_id=designation_id)
                for site in site_list:
                    site_id = sit.objects.get(site_id=int(site))
                    employee_site.objects.create(employee_id=employeeId,site_id=site_id)

                params = [
                    employeeId, 
                    employeeName, 
                    mobile_no,
                    email, 
                    address,
                    city,
                    state1,
                    pincode,
                    company_id1,
                    account_holder_name,
                    account_no,
                    bank_name,
                    branch_name,
                    ifsc_code,
                    pf_no,
                    uan_no,
                    esic,
                    gender,
                    handicapped,
                    # employeeStatus,
                    # activebtn
                ]
                
                cursor.callproc("stp_insert_employee_master", params)
                for result in cursor.stored_results():
                        datalist = list(result.fetchall())
                if datalist[0][0] == "success":
                    messages.success(request, 'Data successfully entered !')
                else: messages.error(request, datalist[0][0])
            else:
                id = request.POST.get('id', '')
                employee_id = request.POST.get('employee_id', '')
                employee_name = request.POST.get('employee_name', '')
                mobile_no = request.POST.get('mobile_no', '')
                email = request.POST.get('email', '')
                gender = request.POST.get('gender', '')
                handicapped = request.POST.get('handicapped_value', '')
                address = request.POST.get('address', '')
                city = request.POST.get('city', '')
                state1 = request.POST.get('state_id', '')
                pincode = request.POST.get('pincode', '')
                company_id1 = request.POST.get('company_id', '')
                account_holder_name = request.POST.get('account_holder_name', '')
                account_no = request.POST.get('account_no', '')
                bank_name = request.POST.get('bank_name', '')
                branch_name = request.POST.get('branch_name', '')
                ifsc_code = request.POST.get('ifsc_code', '')
                pf_no = request.POST.get('pf_no', '')
                uan_no = request.POST.get('uan_no', '')
                esic = request.POST.get('esic', '')
                employee_status = request.POST.get('employment_status', '')
                is_active = 1 if request.POST.get('is_active', '') == 'on' else 0 
                designation_list = request.POST.getlist('designation_name', '')
                site_list = request.POST.getlist('site_name', '')
                            
                params = [ id,employee_id, employee_name, mobile_no,email, address,city,state1,pincode,account_holder_name,account_no,bank_name,branch_name,ifsc_code,pf_no,uan_no,esic,gender,handicapped,company_id1,employee_status,is_active]    
                # cursor.callproc("stp_update_employee_master",params) 
                # messages.success(request, "Data successfully Updated!")

                 
                cursor.callproc("stp_update_employee_master", params)
                for result in cursor.stored_results():
                        datalist = list(result.fetchall())
               # Updating designations for the employee
                        
                employee_designation.objects.filter(employee_id=employee_id).delete()  # Replace with your actual model

                # Insert new rows with the employee_id and designation_id
                for designation_idd in designation_list:
                    # Create a new instance of the model with the employee_id and designation_id
                    designation_id1 = get_object_or_404(designation_master, designation_id=designation_idd)
                    new_entry = employee_designation(employee_id=employee_id, designation_id=designation_id1)
                    new_entry.save()

                # Deleting the existing sites for the employee
                employee_site.objects.filter(employee_id=employee_id).delete()

                # Updating sites for the employee
                for site_idd in site_list:
                    # Fetching the correct site using the 'id' field (or the correct field name)
                    site_id1 = get_object_or_404(sit, site_id=site_idd)
                    
                    # Creating a new employee-site relation
                    new_entry = employee_site(employee_id=employee_id, site_id=site_id1)
                    new_entry.save()

                
                if datalist[0][0] == "success":
                    messages.success(request, 'Data successfully Updated !')
                else: messages.error(request, datalist[0][0])

    except Exception as e:
        print(f"Error: {e}")  # Temporary for debugging
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        cursor.callproc("stp_error_log", [fun, str(e), user])  
        messages.error(request, 'Oops...! Something went wrong!')


    
    finally:
        cursor.close()
        m.commit()
        m.close()
        Db.closeConnection()
        if request.method=="GET":
            return render(request, "Master/employee_master.html", context)
        elif request.method=="POST":  
            return redirect(f'/masters?entity=em&type=i')

@login_required  
def upload_excel(request):

     if request.method == 'POST' and request.FILES.get('excelFile'):
        excel_file = request.FILES['excelFile']
        file_name = excel_file.name
       # Read the Excel file into three separate DataFrames
        df = pd.read_excel(excel_file)
        
        # Concatenate the three DataFrames into one
      
        # Calculate the total number of rows
        total_rows = len(df)

        update_count = error_count = success_count = 0
        checksum_id = None
        r=None
        global user
        user  = request.session.get('user_id', '')
        try:
            Db.closeConnection()
            m = Db.get_connection()
            cursor = m.cursor()
            entity = request.POST.get('entity', '')
            type = request.POST.get('type', '')
            company_id = request.POST.get('company_id','')
            # state_id=request.POST.get('state_id', None)
            cursor.callproc("stp_get_masters", [entity, type, 'sample_xlsx',user])
            for result in cursor.stored_results():
                columns = [col[0] for col in result.fetchall()]
            # if not all(col in df.columns for col in columns):
            #     messages.error(request, 'Oops...! The uploaded Excel file does not contain the required columns.!')
            #     return redirect(f'/masters?entity={entity}&type={type}')
            upload_for = {'em': 'employee master','um': 'employee master upload','sm': 'site master','cm': 'company master','r': 'roster'}[entity]
            cursor.callproc('stp_insert_checksum', (upload_for,company_id,str(datetime.now().month),str(datetime.now().year),file_name))
            for result in cursor.stored_results():
                c = list(result.fetchall())
            checksum_id = c[0][0]
        
            if entity == 'um':
                for index, row in df.iterrows():
                    row_filtered = row.drop(['worksite', 'designation'], errors='ignore')
                    params = tuple(str(row_filtered.get(column, '')) for column in columns if column not in ['worksite', 'designation'])
                    # After validation, add company_id to params
                    params += (str(company_id),)
                    merged_list = list(zip(columns, params))
                    
                    print(merged_list)
                    
                    # Loop through each (column, value) pair in the merged_list for custom validation
                    for column, value in merged_list:
                        cursor.callproc('stp_employee_validation', [column,value])
                        for result in cursor.stored_results():
                            r = list(result.fetchall())
                        if r and r[0][0] not in ("", None, " ", "Success"):
                            cursor.callproc('stp_insert_error_log', [upload_for, company_id, file_name, datetime.now().date(), str(r[0][0]), checksum_id])
                            error_count += 1
                            
                    for result in cursor.stored_results():
                           cursor.callproc('stp_employeeinsertexcel', params)

                    # Fetch all stored results
                    for result in cursor.stored_results():
                        r = list(result.fetchall())
                       
                        if r:
                            # Ensure the result has data and is not empty
                            if len(r[0]) > 0:
                                result_value = r[0][0]
                                print("Processing result:", result_value)
                                
                #   this is for designation insert  
                
                    print("Columns in DataFrame:", df.columns)

                   
                print("Original Columns in DataFrame:", df.columns)

                
                df.columns = df.columns.str.strip()  


                if 'Employee Id' in df.columns and 'Designation' in df.columns:
                    print("Both 'employee id' and 'designation' found in DataFrame.")

                   
                    df_designations = df[['Employee Id', 'Designation']].dropna(subset=['Designation']).copy()
                    df_designations['company_id'] = company_id  
                    
                    for index, row in df_designations.iterrows():
                        employee_id = row['Employee Id']
                        designations = row['Designation'].split(',')  

                       
                        for designation in designations:
                            designation = designation.strip()  
                            
                            
                            cursor.callproc('stp_insert_employee_designation', [employee_id, designation, company_id])

                          
                            for result in cursor.stored_results():
                                r = list(result.fetchall())

                            if r:
                                result_value = r[0][0]  

                                if result_value == "success":
                                    success_count += 1
                                elif result_value == "updated":
                                    update_count += 1
                                elif result_value.startswith("error"):
                                    # Log the error message in your error log table
                                    error_message = result_value  # The error message from the procedure
                                    cursor.callproc('stp_insert_error_log', [
                                        upload_for, company_id, file_name, datetime.now().date(), error_message, checksum_id
                                    ])
                                    error_count += 1  # Increment error count for errors

                else:
                    # In case 'employee id' or 'designation' is missing in df.columns
                    print("Required columns 'employee id' or 'designation' not found in the DataFrame.")

                       #   this is for worksite insert  
                if 'Employee Id' in df.columns and 'Worksite' in df.columns:
                    print("Both 'employee id' and 'worksite' found in DataFrame.")

                    # Create a second DataFrame for 'employee_id', 'designation', and company_id
                    df_worksite = df[['Employee Id', 'Worksite']].dropna(subset=['Worksite']).copy()
                    df_worksite['company_id'] = company_id  # Add company_id to df_designations

                    # Loop through each row in the DataFrame
                    for index, row in df_worksite.iterrows():
                        employee_id = row['Employee Id']
                        worksite = row['Worksite'].split(',')  # Assuming multiple designations are comma-separated

                        # Loop through each designation and insert it into the employee_designation table
                        for worksite in worksite:
                            worksite = worksite.strip()  # Trim spaces from the designation
                            
                            # Call the stored procedure to insert the designation for the employee
                            cursor.callproc('stp_insert_employee_site', [employee_id, worksite, company_id])

                            # Fetch all stored results to check the response from the procedure
                            for result in cursor.stored_results():
                                r = list(result.fetchall())

                            if r:
                                result_value = r[0][0]  # Fetch the result from the stored procedure

                                if result_value == "success":
                                    success_count += 1
                                elif result_value == "updated":
                                    update_count += 1
                                elif result_value.startswith("error"):
                                    # Log the error message in your error log table
                                    error_message = result_value  # The error message from the procedure
                                    cursor.callproc('stp_insert_error_log', [
                                        upload_for, company_id, file_name, datetime.now().date(), error_message, checksum_id
                                    ])
                                    error_count += 1  # Increment error count for errors

                else:
                    # In case 'employee id' or 'designation' is missing in df.columns
                    print("Required columns 'employee id' or 'worksite' not found in the DataFrame.")


                          
            elif entity == 'sm':
                for index,row in df.iterrows():
                    params = tuple(str(row.get(column, '')) for column in columns)
                    params += (str(company_id),)
                    cursor.callproc('stp_insert_site_master', params)
                    for result in cursor.stored_results():
                            r = list(result.fetchall())
                    if r[0][0] not in ("success", "updated"):
                        cursor.callproc('stp_insert_error_log', [upload_for, company_id,file_name,datetime.now().date(),str(r[0][0]),checksum_id])
                    if r[0][0] == "success": success_count += 1 
                    elif r[0][0] == "updated": update_count += 1  
                    else: error_count += 1
                    
            elif entity == 'cm':
                for index,row in df.iterrows():
                    params = tuple(str(row.get(column, '')) for column in columns)
                    cursor.callproc('stp_insert_company_master', params)
                    for result in cursor.stored_results():
                            r = list(result.fetchall())
                    if r[0][0] not in ("success", "updated"):
                        cursor.callproc('stp_insert_error_log', [upload_for, company_id,file_name,datetime.now().date(),str(r[0][0]),checksum_id])
                    if r[0][0] == "success": success_count += 1 
                    elif r[0][0] == "updated": update_count += 1  
                    else: error_count += 1
            checksum_msg = f"Total Rows Processed: {total_rows}, Successful Entries: {success_count}" f"{f', Updates Entries: {update_count}' if update_count > 0 else ''}" f"{f', Errors Columnwise: {error_count}' if error_count > 0 else ''}"
            cursor.callproc('stp_update_checksum', (upload_for,company_id,'',str(datetime.now().month),str(datetime.now().year),file_name,checksum_msg,error_count,update_count,checksum_id))
            if error_count == 0 and update_count == 0 and success_count > 0:
                messages.success(request, f"All data uploaded successfully!.")
            elif error_count == 0 and success_count == 0 and update_count > 0:
                messages.warning(request, f"All data updated successfully!.")
            else:messages.warning(request, f"The upload processed {total_rows} rows, resulting in {success_count} successful entries"  f"{f', {update_count} updates' if update_count > 0 else ''}" f", and {error_count} errors; please check the error logs for details.")
                   
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            fun = tb[0].name
            cursor.callproc("stp_error_log", [fun, str(e), user])  
            messages.error(request, 'Oops...! Something went wrong!')
            m.commit()   
        finally:
            cursor.close()
            m.close()
            Db.closeConnection()
            if entity=='um':
                return redirect(f'/masters?entity=em&type=i')
            else:
                return redirect(f'/masters?entity={entity}&type=i')

def get_access_control(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    company = []
    worksite = []
    global user
    user  = request.session.get('user_id', '')
    try:
        if request.method == "POST":
            type = request.POST.get('type','')
            ur = request.POST.get('ur', '')
            cursor.callproc("stp_get_access_control_val", [type,ur,'company'])
            for result in cursor.stored_results():
                company = list(result.fetchall())
            cursor.callproc("stp_get_access_control_val", [type,ur,'worksite'])
            for result in cursor.stored_results():
                worksite = list(result.fetchall())
            if type == 'worksites':
                company_id = request.POST.getlist('company_id','')
                company_ids = ','.join(company_id)
                cursor.callproc("stp_get_access_control_val", [type,company_ids,'worksites'])
                for result in cursor.stored_results():
                    worksite = list(result.fetchall())
                    
            response = {'result': 'success', 'company': company, 'worksite': worksite}
        else: response = {'result': 'fail', 'message': 'Invalid request method'}

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        cursor.callproc("stp_error_log", [tb[0].name, str(e), user])
        print(f"error: {e}")
        response = {'result': 'fail', 'message': 'Something went wrong!'}

    finally:
        cursor.close()
        m.close()
        Db.closeConnection()
        return JsonResponse(response)
class RosterDataAPIView(APIView):
    # Ensure the user is authenticated using JWT
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        # Extract user ID from the JWT token
        user = request.user  # This will get the user from the JWT token

        # Call the function to get the roster data
        roster_data = self.get_roster_data(user.id)
        Log.objects.create(log_text=f"Fetched user by ID: {user.id}")

        return Response(roster_data)

    def get_roster_data(self, user_id):
        # Step 1: Get the user by user_id
        user = CustomUser.objects.get(id=user_id)
        
        # Step 2: Get the phone number of the user
        phone_number = user.phone

        # Step 3: Get the employee_id from sc_employee_master using the phone number
        try:
            employee = sc_employee_master.objects.get(mobile_no=phone_number)
        except sc_employee_master.DoesNotExist:
            return {
                'error': 'Employee not found'
            }
        employee_id = employee.employee_id

        # Step 4: Get the current date and the first date of the current month
        current_date = timezone.now().date()

        # Step 5: Query sc_roster for the current month and categorize the data
        current_roster_qs = sc_roster.objects.filter(
            employee_id=employee_id,
            shift_date__gte=current_date,
            shift_time__isnull=False
        )
        
        current_roster_qsser = ScRosterSerializer(current_roster_qs, many=True)

        previous_roster_qs = sc_roster.objects.filter(
            employee_id=employee_id,
            shift_date__lt=current_date,
            shift_time__isnull=False
            
        )
        previous_roster_qsser = ScRosterSerializer(previous_roster_qs, many=True)

        marked_roster_qs = sc_roster.objects.filter(
            employee_id=employee_id,
            confirmation__isnull=False ,
            shift_time__isnull=False
        )
        marked_roster_qsser = ScRosterSerializer(marked_roster_qs, many=True)

        unmarked_roster_qs = sc_roster.objects.filter(
            employee_id=employee_id,
            confirmation__isnull=True ,
            shift_date__lt=current_date,
            shift_time__isnull=False
        )
        unmarked_roster_qsser = ScRosterSerializer(unmarked_roster_qs, many=True)

        # Count the number of rows in each query set
        current_roster_count = len(current_roster_qsser.data)
        previous_roster_count = len(previous_roster_qsser.data)
        marked_roster_count = len(marked_roster_qsser.data)
        unmarked_roster_count = len(unmarked_roster_qsser.data)

        # Return the counts and the lists
        return {
            'current_roster_count': current_roster_count,
            'current_roster_list': list(current_roster_qsser.data ),  # Using .values() to serialize queryset
            'previous_roster_count': previous_roster_count,
            'previous_roster_list': list(previous_roster_qsser.data),  # Using .values() to serialize queryset
            'marked_roster_count': marked_roster_count,
            'marked_roster_list': list(marked_roster_qsser.data),  # Using .values() to serialize queryset
            'unmarked_roster_count': unmarked_roster_count,
            'unmarked_roster_list': list(unmarked_roster_qsser.data),  # Using .values() to serialize queryset
            'roster_list': list(current_roster_qsser.data)  # Same as Current Roster List
        }
    
class SlotDataAPIView(APIView):
    # Ensure the user is authenticated using JWT
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        # Extract user ID from the JWT token
        user = request.user  # This will get the user from the JWT token

        # Call the function to get the roster data
        slot_data = self.get_slot_data(user.id)
        Log.objects.create(log_text=f"Fetched user by ID: {user.id}")

        return Response(slot_data)

    def get_slot_data(self, user_id):
        # Close any previous connections and get a new one
        Db.closeConnection()
        m = Db.get_connection()
        cursor = m.cursor()

        # Step 1: Retrieve the user
        try:
            user = CustomUser.objects.get(id=user_id)
            phone_number = user.phone
        except CustomUser.DoesNotExist:
            return {'error': 'User not found'}

        try:
            employee = sc_employee_master.objects.get(mobile_no=phone_number)
            employee_id = employee.employee_id
            company_idd = employee.company_id.company_id
        except sc_employee_master.DoesNotExist:
            return {'error': 'Employee not found'}

        # Step 3: Retrieve all UserSlotDetails entries for the given employee and company
        try:
            user_slot_details = UserSlotDetails.objects.filter(employee_id=employee_id, company_id=company_idd)
            user_slot_data = UserSlotDetailsSerializer(user_slot_details, many=True).data
 
            user_alloted_count = len(user_slot_data)

            user_attendance_details = slot_attendance_details.objects.filter(employee_id=employee_id, company_id=company_idd)
            user_attendance_data = UserSlotDetailsSerializer(user_attendance_details, many=True).data

            user_attendance_count = len(user_attendance_data)

            designation_ids = employee_designation.objects.filter(employee_id=employee_id).values_list('designation_id', flat=True)
            site_ids = employee_site.objects.filter(employee_id=employee_id).values_list('site_id', flat=True)
            slot_details = SlotDetails.objects.filter(
                designation_id__in=designation_ids,
                site_id__in=site_ids
            )

            # slot_details_list1 = SlotListDetailsSerializer(slot_details, many=True).data
            # slot_ids = slot_details.values_list('slot_id', flat=True)

            # setting_master_details = SettingMaster.objects.filter(slot_id__in=slot_ids)
            # slot_details_list = SettingMasterSerializer(setting_master_details, many=True).data

            # slot_id_counts = UserSlotDetails.objects.filter(slot_id__in=slot_ids).values('slot_id').annotate(count=Count('id'))

            # # Step 3: Initialize a list to hold the results
            # slot_count_list = []

            # # Step 4: Populate the list with counts
            # # Create a dictionary with slot_id and count initialized to 0
            # slot_count_dict = {slot_id: 0 for slot_id in slot_ids}

            # # Update counts based on the query results
            # for item in slot_id_counts:
            #     slot_count_dict[item['slot_id']] = item['count']

            # # Create the final list of dictionaries
            # for slot_id, count in slot_count_dict.items():
            #     slot_count_list.append({'slotId': slot_id, 'count': count})

            # # Now slot_count_list contains the slotId and its count
            # print(slot_count_list)

            # Step 1: Serialize the slot details
            slot_details_list1 = SlotListDetailsSerializer(slot_details, many=True).data
            slot_ids = slot_details.values_list('slot_id', flat=True)

            # Step 2: Retrieve SettingMaster details
            setting_master_details = SettingMaster.objects.filter(slot_id__in=slot_ids)
            slot_details_list = SettingMasterSerializer(setting_master_details, many=True).data

            matched_slot_ids = setting_master_details.values_list('slot_id', flat=True)

            slot_id_counts = UserSlotDetails.objects.filter(slot_id__in=matched_slot_ids).values('slot_id').annotate(count=Count('id'))

            slot_count_list = []

            slot_count_dict = {slot_id: 0 for slot_id in matched_slot_ids}

            # Update counts based on the query results
            for item in slot_id_counts:
                slot_count_dict[item['slot_id']] = item['count']

            # Create the final list of dictionaries
            for slot_id, count in slot_count_dict.items():
                slot_count_list.append({'employeeId':employee_id,'slotId': slot_id, 'count': count})

            # Now slot_count_list contains the slotId and its count
            print(slot_count_list)


            return {
                'slot_alloted_count': user_alloted_count,
                'slot_alloted_list': list(user_slot_data),
                'user_attendance_count':user_attendance_count,
                'user_attendance_list':list(user_attendance_data),
                'slot_details_list':list(slot_details_list),
                'slot_count_list':slot_count_list,
                'employee_id':employee_id,
            }
        
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            cursor.callproc("stp_error_log", [tb[0].name, str(e), user_id])
            print(f"error: {e}")
            return {'result': 'fail', 'message': 'Something went wrong!'}


        
class confirm_schedule(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    # authentication_classes = []

    def post(self, request):
        try:
            data= request.data
            roster_id = request.data.get('id')
            confirmation = request.data.get('confirmation') == '1'
            user = request.user
            roster = sc_roster.objects.get(id=roster_id)
            roster.confirmation = confirmation
            roster.updated_at = timezone.now()
            roster.confirmation_date = timezone.now()
            roster.updated_by = user
            roster.save()
            ser = ScRosterSerializer(roster)

            return Response({'success': 'Confirmation updated successfully.','data':ser.data,'con':confirmation}, status=200)
        except sc_roster.DoesNotExist:
            return Response({'error': 'Roster not found.'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)



class confirm_notification(APIView):
    # Ensure the user is authenticated using JWT
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    # authentication_classes = []

    def post(self, request):
        try:
            data= request.data
            notification_id = request.data.get('id')
            confirmation = request.data.get('confirmation') == '1'
            user = request.user
            notification = notification_log.objects.get(id=notification_id)
            notification.notification_opened = timezone.now()
            notification.updated_at = timezone.now()
            notification.updated_by = user
            notification.save()

            return Response({'success': 'Confirmation updated successfully.'}, status=200)
        except notification_log.DoesNotExist:
            return Response({'error': 'notification_log not found.'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
@login_required
def slot_details(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor = m.cursor()
    user_id = request.session.get('user_id', '')

    try:
        if request.method == 'GET':
            slot_id = request.GET.get('slot_id', '')
            type = request.GET.get('type', '')

            cursor.callproc("stp_get_dropdown_values", ['company'])
            for result in cursor.stored_results():
                company_names = list(result.fetchall())

            cursor.callproc("stp_get_dropdown_values", ['site'])
            for result in cursor.stored_results():
                site_names = list(result.fetchall())
            
            cursor.callproc("stp_get_dropdown_values", ['designation'])
            for result in cursor.stored_results():
                designation = list(result.fetchall())

            if slot_id == "0":
                context = {'slot_id': slot_id,'company_names': company_names,'site_names': site_names,'designation':designation,'type': type}


        elif request.method == 'POST':
            slot_id = request.POST.get('slot_id', '')
            type = 'shift'
            company_id = request.POST.get('company_id', '')
            site_id = request.POST.get('worksite', '')  

            cursor.callproc("stp_get_dropdown_values", ['designation'])
            for result in cursor.stored_results():
                designation = list(result.fetchall())

            context= {'slot_id':slot_id,'company_id':company_id, 'site_id':site_id,'type':type,'designation':designation}
        
            # messages.success(request, "Slot successfully created!")
            

    except Exception as e:
        tb = traceback.format_exc()  # Capture the full traceback
        cursor.callproc("stp_error_log", [tb, str(e), str(user_id)])  # Log the error with the traceback and user ID
        print(f"error: {e}")
        return JsonResponse({'result': 'fail', 'message': 'Something went wrong!'})

    finally:
        cursor.close()
        m.commit()
        m.close()
        Db.closeConnection()
        return render(request, 'Master/slot_details.html', context)


@login_required 
def post_slot_details(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor = m.cursor()
    user_idd = request.session.get('user_id', '')
    user = CustomUser.objects.get(id=user_idd)  

    try:
        # Load additional shift data from JSON input
        shifts_data = json.loads(request.POST.get('shifts', '[]'))  
        shifts_data2 = json.loads(request.POST.get('shifts2', '[]')) 

        # Gather main shift data from POST request
        slot_name = request.POST.get('slot_name', '')
        description = request.POST.get('description', '')
        shift_date = request.POST.get('shift_date', '')
        start_time = request.POST.get('start_time', '')
        end_time = request.POST.get('end_time', '')
        designation = request.POST.get('designation') # Assuming designation_name is the field name

        night_shift = request.POST.get('night_shift', '0')
        company_id = request.POST.get('company_id', '')
       
        if not shift_date and not shifts_data and not shifts_data2:
            return JsonResponse({'status': 'error', 'message': 'No shift data received.'})

        # Save the main shift if all necessary data is provided
        if shift_date and start_time and end_time:
            initial_shift_detail = SlotDetails(
                slot_name=slot_name,
                slot_description=description,
                shift_date=shift_date,
                start_time=start_time,
                end_time=end_time,
                designation_id=get_object_or_404(designation_master,  designation_id=designation),
                night_shift=bool(int(night_shift)), 
                company_id=company_id,
                site_id=get_object_or_404(sit, site_id=request.POST.get('site_id', '')),
                created_by=user # User reference
            )
            initial_shift_detail.save()

        # Process extra shifts (shifts_data)
        for shift in shifts_data:
            if shift.get('start_time') and shift.get('end_time'):
                shift_detail_add = SlotDetails(
                    slot_name=slot_name,
                    slot_description=description,
                    shift_date=shift_date,
                    designation_id=get_object_or_404(designation_master,  designation_id=designation),
                    start_time=shift.get('start_time'),
                    end_time=shift.get('end_time'),
                    night_shift=bool(int(shift.get('night_shift', '0'))), 
                    company_id=company_id,
                    site_id= get_object_or_404(sit, site_id=request.POST.get('site_id', '')),
                    created_by=user  # User reference
                )
                shift_detail_add.save()

        # Process multiple shifts (shifts_data2)
        for shift2 in shifts_data2:
            if shift2.get('shiftDate') and shift2.get('startTime') and shift2.get('endTime'):
                shift_detail_add = SlotDetails(
                    slot_name=shift2.get('new_slot_name'),
                    slot_description=shift2.get('new_description'),
                    designation_id=get_object_or_404(designation_master, designation_id = shift2.get('new_designation')),
                    shift_date=shift2.get('shiftDate'),
                    start_time=shift2.get('startTime'),
                    end_time=shift2.get('endTime'),
                    night_shift=bool(int(shift2.get('nightShift', '0'))), 
                    company_id=company_id,
                    site_id=get_object_or_404(sit, site_id=request.POST.get('site_id', '')),
                    created_by=user
                )
                shift_detail_add.save()

            # Save additional shift times (newStartTime and newEndTime)
            for additional_shift in shift2.get('shiftTimes', []):
                if additional_shift.get('newStartTime') and additional_shift.get('newEndTime'):
                    shift_detail_additional = SlotDetails(
                        slot_name=shift2.get('new_slot_name'),
                        slot_description=shift2.get('new_description'),
                        designation_id=get_object_or_404(designation_master, designation_id = shift2.get('new_designation')),
                        shift_date=shift2.get('shiftDate'),  # Use the same shift date
                        start_time=additional_shift.get('newStartTime'),
                        end_time=additional_shift.get('newEndTime'),
                        night_shift=bool(int(additional_shift.get('newNightShift', '0'))),  
                        company_id=company_id,
                        site_id=get_object_or_404(sit, site_id=request.POST.get('site_id', '')),
                        created_by=user # User reference
                    )
                    shift_detail_additional.save()


        return JsonResponse({'success': True, 'redirect_url': '/masters?entity=sd&type=i'})

    
    except Exception as e:
        tb = traceback.format_exc()  # Get the full traceback as a string
        cursor.callproc("stp_error_log", [tb, str(e), str(user_idd)])  # Log the error with the traceback and user ID
        print(f"error: {e}")
        
    finally:
        cursor.close()
        m.commit()
        m.close()
        Db.closeConnection()
        

@login_required 
def setting_master(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    user_id  = request.session.get('user_id', '')
    user_idd = CustomUser.objects.get(id=user_id)
    try:
        if request.method == 'GET':
            slot_id = request.GET.get('slot_id', '')
            slot_idd = decrypt_parameter(slot_id)
            type = request.GET.get('type', '')
            # setting_id = request.GET.get('setting_id', '')

            try:
                settings_data = get_object_or_404(SettingMaster, slot_id=slot_idd)
                context = {'settings_data': settings_data, 'type': type}
            except Http404:
                context = {'slot_id':slot_id,'type': type} 
            
        elif request.method == 'POST':
            setting_id = request.POST.get('setting_id1', '')
            # slot_id = request.POST.get('slot_id', '')
            # slot_idd = decrypt_parameter(slot_id)
            # slot_id1 = get_object_or_404(SlotDetails, slot_id=slot_idd),
            if setting_id:
                notification = get_object_or_404(SettingMaster, id=setting_id)
                notification.noti_start_time = request.POST.get('notification_start_time', '')
                notification.noti_end_time = request.POST.get('notification_end_time', '')
                notification.no_of_notification = request.POST.get('number_of_notifications', '')
                notification.interval = request.POST.get('notification_interval_hours', '')
                notification.no_of_employee = request.POST.get('employee_count', '')
                notification.updated_by = user_idd
                notification.save()

                messages.success(request, "Slot Settings successfully updated!")
            else:
                notification = SettingMaster(
                noti_start_time= request.POST.get('notification_start_time', ''),
                noti_end_time=request.POST.get('notification_end_time', ''),
                no_of_notification=request.POST.get('number_of_notifications', ''),
                interval = request.POST.get('notification_interval_hours',''),
                no_of_employee = request.POST.get('employee_count',''),
                slot_id = get_object_or_404(slot, slot_id=decrypt_parameter(request.POST.get('slot_id', ''))),
                created_by=user_idd
                )
                notification.save()

                messages.success(request, "Slot Settings successfully Saved!")



    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        cursor.callproc("stp_error_log", [tb[0].name, str(e), user])
        print(f"error: {e}")
        response = {'result': 'fail', 'message': 'Something went wrong!'}
    finally:
        cursor.close()
        m.commit()
        m.close()
        Db.closeConnection()
        if request.method == 'GET':
            return render(request, 'Master/slot_details.html', context)
        elif request.method == 'POST':
            new_url = f'/masters?entity=sd&type=i'
            return redirect(new_url) 

@login_required  
def edit_slot_details(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    user_id  = request.session.get('user_id', '')
    user_idd = CustomUser.objects.get(id=user_id)
        

    try:
        if request.method == 'GET':
            cursor.callproc("stp_get_dropdown_values", ['company'])
            for result in cursor.stored_results():
                company_names = list(result.fetchall())
            cursor.callproc("stp_get_dropdown_values", ['worksite'])
            for result in cursor.stored_results():
                site_names = list(result.fetchall())
            cursor.callproc("stp_get_dropdown_values", ['designation'])
            for result in cursor.stored_results():
                designation = list(result.fetchall())
            slot_id = request.GET.get('slot_id')
            slot_idd = decrypt_parameter(slot_id)
            slot_data = get_object_or_404(SlotDetails, slot_id=slot_idd)
          
            context = {
                'slot_data': slot_data,
                'company_names':company_names,
                'designation':designation,
                'site_names':site_names
            }
        elif request.method == 'POST':
            slot_id = request.POST.get('slot_id')
            slot_data = get_object_or_404(SlotDetails, slot_id=slot_id)
            company_id = request.POST.get('company_id')
            slot_name = request.POST.get('slot_name')
            description = request.POST.get('description')
            shift_date  = request.POST.get('shift_date')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            designation_id=request.POST.get('designation')
            night_shift = 1 if request.POST.get('night_shift') == 'on' else 0

            current_date = date.today()  # Get the current date

            setting = get_object_or_404(SettingMaster, slot_id=slot_id)
            noti_start_time = setting.noti_start_time  

            if current_date > noti_start_time:  # Compare current date with noti_start_time
                messages.error(request, "You Cannot Update Data as Notification Time has Started.")
                return
                
            slot_data.company_id = company_id
            slot_data.site_id = get_object_or_404(sit, site_id=request.POST.get('site_id',''))
            slot_data.designation_id = get_object_or_404(designation_master, designation_id=designation_id)
            slot_data.slot_name = slot_name
            slot_data.slot_description = description
            slot_data.shift_date = shift_date
            slot_data.start_time = start_time
            slot_data.end_time = end_time
            slot_data.night_shift = night_shift
            slot_data.updated_by = user_idd

            # Save the updated slot details to the database
            slot_data.save()

            # Show success message and redirect
            messages.success(request, "Slot details updated successfully.")
            
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        cursor.callproc("stp_error_log", [tb[0].name, str(e), user])
        print(f"error: {e}")
        response = {'result': 'fail', 'message': 'Something went wrong!'}
    finally:
        cursor.close()
        m.commit()
        m.close()
        Db.closeConnection()
        if request.method=="GET":
            return render(request, 'Master/edit_slot_details.html', context)
        if request.method=="POST":
            new_url = f'/masters?entity=sd&type=i'
            return redirect(new_url) 
        

def delete_slot(request):
    Db.closeConnection()  
    m = Db.get_connection()
    cursor = m.cursor()

    try:
        slot_id = request.POST.get('slot_id')
        slot_idd = decrypt_parameter(slot_id)

        slots_to_delete = SlotDetails.objects.filter(slot_id=slot_idd)
        setting = get_object_or_404(SettingMaster, slot_id=slot_idd)
        noti_start_time = setting.noti_start_time  

        current_date = date.today()

        if current_date >= noti_start_time:  
            return JsonResponse({'success': False, 'message': 'Slot Cannot be deleted,Because Notification time has begun!'})

        if slots_to_delete.exists():
            slots_to_delete.delete()
            setting.delete()
            return JsonResponse({'success': True, 'message': 'Slot  and its setttings successfully deleted!'})
        else:
            return JsonResponse({'success': False, 'message': 'No slots found with the specified slot_id.'})

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        cursor.callproc("stp_error_log", [tb[0].name, str(e), request.user.username])  

        return JsonResponse({'success': False, 'message': 'An error occurred while deleting the slot.'})

def view_employee(request):
    Db.closeConnection()  
    m = Db.get_connection()
    cursor = m.cursor()
    try:
        if request.method == "GET":
            id = request.GET.get('id', '')

            # Initialize context variable before starting to populate it
            context = {
                'id': id,
                'employee_status': [],
                'employee_status_id': '',
                'site_name': [],
                'gender': [],
                'company_names': [],
                'state_names': [],
                'designation_name': [],
                'employee_id': None,
                'employee_name': None,
                'mobile_no': None,
                'email': None,
                'gender_value': None,
                'state_id_value': None,
                'city': None,
                'address': None,
                'pincode': None,
                'account_holder_name': None,
                'account_no': None,
                'bank_name': None,
                'branch_name': None,
                'ifsc_code': None,
                'pf_no': None,
                'uan_no': None,
                'esic': None,
                'employment_status_id': None,
                'handicapped_value': None,
                'is_active': None,
                'company_id_value': None,
                'selected_designation': [],
                'selected_site': []
            }

            # Populate dropdown values
            cursor.callproc("stp_get_employee_status")
            for result in cursor.stored_results():
                context['employee_status'] = list(result.fetchall())

            cursor.callproc("stp_get_dropdown_values", ('site',))
            for result in cursor.stored_results():
                context['site_name'] = list(result.fetchall())

            cursor.callproc("stp_get_dropdown_values", ('company',))
            for result in cursor.stored_results():
                context['company_names'] = list(result.fetchall())

            cursor.callproc("stp_get_dropdown_values", ('states',))
            for result in cursor.stored_results():
                context['state_names'] = list(result.fetchall())

            cursor.callproc("stp_get_dropdown_values", ('gender',))
            for result in cursor.stored_results():
                context['gender'] = list(result.fetchall())

            cursor.callproc("stp_get_dropdown_values", ('designation',))
            for result in cursor.stored_results():
                context['designation_name'] = list(result.fetchall())

           

            # Otherwise, we are editing an existing employee
            id1 = request.GET.get('id', '')
            id = decrypt_parameter(id1)

            cursor.callproc("stp_edit_employee_master", (id,))
            for result in cursor.stored_results():
                data = result.fetchall()[0]
                context.update({
                    'employee_id': data[0],
                    'employee_name': data[1],
                    'mobile_no': data[2],
                    'email': data[3],
                    'gender_value': data[4],
                    'state_id_value': data[5],
                    'city': data[6],
                    'address': data[7],
                    'pincode': data[8],
                    'account_holder_name': data[9],
                    'account_no': data[10],
                    'bank_name': data[11],
                    'branch_name': data[12],
                    'ifsc_code': data[13],
                    'pf_no': data[14],
                    'uan_no': data[15],
                    'esic': data[16],
                    'employment_status_id': data[17],
                    'handicapped_value': data[18],
                    'is_active': data[19],
                    'company_id_value': data[20],
                })

                # Get the employee's designation and site info
                employee_id = context['employee_id']
                designation_list = employee_designation.objects.filter(employee_id=employee_id)
                context['selected_designation'] = json.dumps(list(map(str, designation_list.values_list('designation_id', flat=True))))

                site_list = employee_site.objects.filter(employee_id=employee_id)
                context['selected_site'] = json.dumps(list(map(str, site_list.values_list('site_id', flat=True))))

    except Exception as e:
        print(f"Error: {e}")  # Temporary for debugging
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        cursor.callproc("stp_error_log", [fun, str(e), user])  
        messages.error(request, 'Oops...! Something went wrong!')

    finally:
        cursor.close()
        m.commit()
        m.close()
        Db.closeConnection()

        if request.method == "GET":
            return render(request, "Master/employee_view.html", context)
        elif request.method == "POST":  
            return redirect(f'/masters?entity=em&type=i')
        

@login_required        
def designation_master1(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    global user
    
    # user_id = request.session.get('user_id', '')
    # user = CustomUser.objects.get(id=user_id)
    try:
        
        if request.method == "GET":
           
            designation_id = request.GET.get('designation_id', '')
            if designation_id == "0":
                if request.method == "GET":
                    context = {'designation_id':designation_id}

            else:
                designation_id = request.GET.get('designation_id', '')
                designation_id = decrypt_parameter(designation_id)
                cursor.callproc("stp_designationedit", (designation_id,))
                for result in cursor.stored_results():
                    data = result.fetchall()[0]  
                    context = {
                        'designation_id': data[0],
                        'designation_name': data[1],
                        'is_active':data[2]
                    }

        if request.method == "POST" :
            id = request.POST.get('designation_id', '')
            if id == '0':
                designation_name = request.POST.get('designation_name', '')
                # is_active = request.POST.get('is_active', '') 
                params = [
                    designation_name,
                    # is_active  
                ]
                cursor.callproc("stp_designationinsert", params)
                for result in cursor.stored_results():
                        datalist = list(result.fetchall())
                if datalist[0][0] == "success":
                    messages.success(request, 'Data successfully entered !')
                else: messages.error(request, datalist[0][0])
            else:
                designation_id = request.POST.get('designation_id', '')
                designation_name = request.POST.get('designation_name', '')
                # is_active1 = request.POST.get('is_active', '')
                is_active = 1 if request.POST.get('is_active') == 'on' else 0 
                            
                params = [designation_id,designation_name,is_active]    
                cursor.callproc("stp_designationupdate",params) 
                messages.success(request, "Data successfully Updated!")

    except Exception as e:
        print(f"Error: {e}")  # Temporary for debugging
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        cursor.callproc("stp_error_log", [fun, str(e), user])  
        messages.error(request, 'Oops...! Something went wrong!')

    finally:
        cursor.close()
        m.commit()
        m.close()
        Db.closeConnection()

        if request.method == "GET":
            return render(request, "Master/designation_master.html", context)
        elif request.method == "POST":  
            return redirect(f'/masters?entity=dm&type=i')

def view_designation(request):
    Db.closeConnection()  
    m = Db.get_connection()
    cursor = m.cursor()
    try:
        if request.method == "GET":
            designation_id = request.GET.get('designation_id', '')

            # Initialize context variable before starting to populate it
            context = {
                'designation_id': None,
                'designation_name': None,
                'is_active': None
            }

            # Otherwise, we are editing an existing employee
            designation_id1 = request.GET.get('designation_id', '')
            designation_id = decrypt_parameter(designation_id1)

            cursor.callproc("stp_designationedit", (designation_id,))
            for result in cursor.stored_results():
                data = result.fetchall()[0]
                context.update({
                    'designation_id': data[0],
                    'designation_name': data[1],
                    'is_active': data[2],
                })


    except Exception as e:
        print(f"Error: {e}")  # Temporary for debugging
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        cursor.callproc("stp_error_log", [fun, str(e), user])  
        messages.error(request, 'Oops...! Something went wrong!')

    finally:
        cursor.close()
        m.commit()
        m.close()
        Db.closeConnection()

        if request.method == "GET":
            return render(request, "Master/designation_view.html", context)
        elif request.method == "POST":  
            return redirect(f'/masters?entity=dm&type=i')

@login_required
def employee_upload(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    pre_url = request.META.get('HTTP_REFERER')
    header, data = [], []
    entity, type, name = '', '', ''
    global user
    user  = request.session.get('user_id', '')
    try:
         
        if request.method=="GET":
            entity = request.GET.get('entity', '')
            type = request.GET.get('type', '')
            
            
            cursor.callproc("stp_get_masters", [entity, type, 'header',user])
            for result in cursor.stored_results():
                header = list(result.fetchall())
            cursor.callproc("stp_get_masters",[entity,type,'data',user])
            for result in cursor.stored_results():
                 data = list(result.fetchall())
            cursor.callproc("stp_get_dropdown_values",['site'])
            for result in cursor.stored_results():
                site_name = list(result.fetchall())
            cursor.callproc("stp_get_dropdown_values",['designation'])
            for result in cursor.stored_results():
                designation_name = list(result.fetchall())
            cursor.callproc("stp_get_dropdown_values",['company'])
            for result in cursor.stored_results():
                company_names = list(result.fetchall())
            cursor.callproc("stp_get_dropdown_values",['states'])
            for result in cursor.stored_results():
                state_name = []
                state_name = list(result.fetchall())
                

        if request.method=="POST":
            entity = request.POST.get('entity', '')
            type = request.POST.get('type', '')
            if entity == 'r' and type == 'ed':
                ids = request.POST.getlist('ids[]', '')
                shifts = request.POST.getlist('shifts[]', '')
                for id,shift in zip(ids, shifts):
                    cursor.callproc("stp_post_roster",[id,shift])
                    for result in cursor.stored_results():
                        datalist = list(result.fetchall())
                if datalist[0][0] == "success":
                    messages.success(request, 'Data updated successfully !')
            if entity == 'urm' and (type == 'acu' or type == 'acr'):
                
                created_by = request.session.get('user_id', '')
                ur = request.POST.get('ur', '')
                selected_company_ids = list(map(int, request.POST.getlist('company_id')))
                selected_worksites  = request.POST.getlist('worksite')
                company_worksite_map = {}
                
                if not selected_company_ids or not selected_worksites:
                    messages.error(request, 'Company or worksite data is missing!')
                    return redirect(f'/masters?entity={entity}&type=urm')
                if type not in ['acu', 'acr'] or not ur:
                    messages.error(request, 'Invalid data received.')
                    return redirect(f'/masters?entity={entity}&type=urm')
                
                cursor.callproc("stp_get_company_worksite",[",".join(request.POST.getlist('company_id'))])
                for result in cursor.stored_results():
                    company_worksites  = list(result.fetchall())
                    
                for company_id, worksite_name in company_worksites:
                    if company_id not in company_worksite_map:
                        company_worksite_map[company_id] = []
                    company_worksite_map[company_id].append(worksite_name)
                
                filtered_combinations = []
                for company_id in selected_company_ids:
                    valid_worksites = company_worksite_map.get(company_id, [])
                    # Filter worksites that were actually selected by the user
                    selected_valid_worksites = [ws for ws in selected_worksites if ws in valid_worksites]
                    filtered_combinations.extend([(company_id, ws) for ws in selected_valid_worksites])
                    
                cursor.callproc("stp_delete_access_control",[type,ur])
                r=''
                for company_id, worksite in filtered_combinations:
                    cursor.callproc("stp_post_access_control",[type,ur,company_id,worksite,created_by])
                    for result in cursor.stored_results():
                            r = list(result.fetchall())
                type='urm'
                if r[0][0] == "success":
                    messages.success(request, 'Data updated successfully !')
                
            else : messages.error(request, 'Oops...! Something went wrong!')
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        cursor.callproc("stp_error_log",[fun,str(e),user])  
        messages.error(request, 'Oops...! Something went wrong!')
    finally:
        cursor.close()
        m.commit()
        m.close()
        Db.closeConnection()
        if request.method=="GET":
            return render(request,'Master/employee_upload.html', {'entity':entity,'type':type,'name':name,'header':header,'company_names':company_names,'state_name':state_name,'site_name':site_name,'designation_name':designation_name,'data':data,'pre_url':pre_url})
        elif request.method=="POST":  
            new_url = f'/masters1?entity={entity}&type={type}'
            return redirect(new_url)      



class EmployeeData(APIView):
    # Ensure the user is authenticated using JWT
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        # Get parameters from the request
        employee_id = request.data['employee_id']
        company_id = request.data['company_id']

        try:
            # Fetch the employee using the provided parameters
            employee = sc_employee_master.objects.filter(employee_id=employee_id, company_id=company_id).first()

            if employee:
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data)
            else:
                return Response({"error": "Employee not found"}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def put(self, request, *args, **kwargs):
        # Get employee_id and company_id from the request
        employee_id = request.data.get('employee_id')
        company_id = request.data.get('company_id')

        try:
            # Fetch the employee using the provided parameters
            employee = sc_employee_master.objects.filter(employee_id=employee_id, company_id=company_id).first()

            if not employee:
                return Response({"error": "Employee not found"}, status=404)
            vv = request.data.get('state_id', employee.state_id)
            cc = get_object_or_404(StateMaster,  state_id=vv)    
            # Update only the fields that are provided in the request
            employee.email = request.data.get('email', employee.email)
            employee.address = request.data.get('address', employee.address)
            employee.city = request.data.get('city', employee.city)
            employee.state_id=cc
            employee.account_holder_name = request.data.get('account_holder_name', employee.account_holder_name)
            employee.account_no = request.data.get('account_no', employee.account_no)
            employee.bank_name = request.data.get('bank_name', employee.bank_name)
            employee.branch_name = request.data.get('branch_name', employee.branch_name)
            employee.ifsc_code = request.data.get('ifsc', employee.ifsc_code)

            # Save the updated employee record
            employee.save()

            return Response({"success": "Employee data updated successfully"}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
class StateName(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            states = StateMaster.objects.all()  
            serializer = StateMasterSerializer(states, many=True)  
            return Response(serializer.data)  
        except Exception as e:
            return Response({"error": str(e)},  status=404)



def deactivate_slot(request):
    Db.closeConnection()  
    m = Db.get_connection()
    cursor = m.cursor()
    user_id  = request.session.get('user_id', '')
    user_idd = CustomUser.objects.get(id=user_id)
    try:
        if request.method == 'POST':
            slot_id = request.POST.get('slot_id')
            slot_idd = decrypt_parameter(slot_id)
            reason = request.POST.get('reason', '') 

            slot_detail = SlotDetails.objects.get(slot_id=slot_idd)  
            slot_detail.is_active = 0
            slot_detail.message = reason 
            slot_detail.updated_by = user_idd
            slot_detail.save()

            return JsonResponse({'message': 'Slot deactivated successfully.'})
    except SlotDetails.DoesNotExist:
        return JsonResponse({'message': 'Slot ID not found.'}, status=404)
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        cursor.callproc("stp_error_log", [tb[0].name, str(e), request.user.username])
        return JsonResponse({'message': str(e)}, status=500)
    
    finally:
        cursor.close()
        m.commit()
        m.close()
        Db.closeConnection()


class post_user_slot(APIView):
    
    def post(self, request):
        Db.closeConnection()  
        m = Db.get_connection()
        cursor = m.cursor()
        # Extracting the user id from the session
        try:
        
            # Extracting data from the request
            employee_id = request.data.get('employee_id')
            slot = request.data.get('slot_id')
            site = request.data.get('site_id')
            slot_id = get_object_or_404(SlotDetails, slot_id=slot)
            company = get_object_or_404(com, company_id=request.data.get('company_id'))
            site = get_object_or_404(sit, site_id=site)

                # Creating a new instance of UserSlotDetails and saving it to the database
            user_slot = UserSlotDetails(
                employee_id=employee_id,
                slot_id=slot_id,
                company_id=company,
                site_id=site,
            )
            user_slot.save()
            return Response({"message": "User slot details created successfully."}, status=200)
        
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            cursor.callproc("stp_error_log", [tb[0].name, str(e), request.user.username])
            return JsonResponse({'message': str(e)}, status=500)




