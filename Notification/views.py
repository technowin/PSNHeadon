import traceback
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.utils.timezone import now
from datetime import time, timedelta

from Masters.models import *
from django.db.models import Q
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
import requests
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import json
import google.auth
from google.oauth2 import service_account
import google.auth.transport.requests
import os

import base64
import json
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from rest_framework import status

from Masters.serializers import ScRosterSerializer, SlotDetailsSerializer, UserSlotDetailsSerializer, UserSlotDetailsSerializer1, UserSlotlistSerializer
from Notification.models import notification_log, user_notification_log
from datetime import datetime, timedelta

from Payroll.models import slot_attendance_details
# Create your views here.
# def check_shift_for_next_day(request, employee_id, site_id):
#     tomorrow = now().date() + timedelta(days=1)
    
#     try:
#         site = site_master.objects.get(site_id=site_id)
        
#         shift = sc_roster.objects.get(employee_id=employee_id, site=site, shift_date=tomorrow)
        
#         response_data = {
#             'has_shift': True,
#             'notification_time': site.notification_time.strftime('%H:%M'),
#             'shift_from': shift.shift_from.strftime('%H:%M'),
#             'shift_to': shift.shift_to.strftime('%H:%M'),
#         }
#     except sc_roster.DoesNotExist:
#         response_data = {'has_shift': False}
    
#     return JsonResponse(response_data)

class check_and_notify_user(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        # Get user from request (JWT token will give us the user)
        user = request.user
        current_time = timezone.now()

        # Get the employee from sc_employee_master based on the user's phone number
        employee = sc_employee_master.objects.filter(mobile_no=user.phone).first()

        if not employee:
            return Response({"message": "Employee not found."}, status=404)

        # Check if there are any shifts for the employee for the next day
        next_day = current_time.date() + timedelta(days=1)
        shifts = sc_roster.objects.filter(employee_id=employee.employee_id, shift_date=next_day)

        if shifts.exists():
            # Send notification logic here
            send_push_notification(user)  # Function to send push notification
            return Response({"message": "Notification sent."}, status=200)
        else:
            return Response({"message": "No shifts found for the next day."}, status=200)

# class check_and_notify_all_users(APIView):
    
#     def get(self, request):
#         users = CustomUser.objects.all()
#         current_time = timezone.now()
#         errors = []
#         success = []
        
#         for user in users:

#             slot_ids = SlotDetails.objects.filter(
#                 Q(designation_id__in=designation_ids) & Q(site_id__in=site_ids)
#             ).values_list('slot_id', flat=True)

#             if user.phone != '8291104778':
#                 continue
#             # Step 1: Fetch employee based on user's phone number
#             employee = sc_employee_master.objects.filter(mobile_no=user.phone).first()
#             if not employee:
#                 continue
            
#             # Step 2: Get site and designation IDs for the employee
#             site_ids = employee_site.objects.filter(employee_id=employee.employee_id).values_list('site_id', flat=True)
#             designation_ids = employee_designation.objects.filter(employee_id=employee.employee_id).values_list('designation_id', flat=True)
            
#             # Step 3: Get slot IDs that match both designation and site IDs
#             slot_ids = SlotDetails.objects.filter(
#                 Q(designation_id__in=designation_ids) & Q(site_id__in=site_ids)
#             ).values_list('slot_id', flat=True)
            
#             # Step 4: Fetch notification settings for each slot ID from SettingMaster
#             notification_settings = SettingMaster.objects.filter(slot_id__in=slot_ids).values(
#                 'slot_id', 'noti_start_time', 'noti_end_time', 'interval', 'no_of_notification'
#             )

#             # Process each notification setting for the slots
#             for setting in notification_settings:
#                 slot_id = setting['slot_id']
#                 noti_start_time = setting['noti_start_time']
#                 noti_end_time = setting['noti_end_time']
#                 interval = setting['interval']
#                 no_of_notification = int(setting['no_of_notification'])
                
#                 current_notification_time = noti_start_time
#                 notifications_sent = 0

#                 # Send notifications at specified intervals
#                 while notifications_sent < no_of_notification and current_notification_time <= noti_end_time:
#                     try:
#                         # Serialize shift data for notification
#                         slot_instance = get_object_or_404(SlotDetails, slot_id=slot_id)
#                         shift_data = SlotDetailsSerializer(slot_instance).data

#                         # Log the notification in user_notification_log
#                         notification_entry = user_notification_log.objects.create(
#                             slot_id=slot_instance,
#                             noti_send_time=timezone.now(),
#                             notification_message="Notification for shift confirmation",
#                             type_id=11,  # Replace with actual type_id if needed
#                             created_by=user,
#                             employee_id = employee.employee_id,
#                             emp_id=get_object_or_404(sc_employee_master, employee_id=employee.employee_id)
#                         )

#                         # Send push notification and handle response
#                         result = send_push_notification(user, shift_data, notification_entry.id)
#                         if result != "success":
#                             # Handle errors in sending notification
#                             response_message = result.split("--")
#                             if len(response_message) == 2:
#                                 error_detail = response_message[1]
#                                 if error_detail == "Requested entity was not found.":
#                                     notification_entry.notification_message = "App Is Not Installed"
#                                 elif error_detail == "The registration token is not a valid FCM registration token":
#                                     notification_entry.notification_message = "User Not Correctly Registered to the App. Please Login Again."
#                                 else:
#                                     notification_entry.notification_message = result
#                             else:
#                                 notification_entry.notification_message = result
                            
#                             notification_entry.save()
#                             errors.append(f"Error sending notification to {user.full_name} - {result}")
#                         else:
#                             notification_entry.noti_receive_time = timezone.now()
#                             notification_entry.save()

#                         interval_minutes = int(interval) 

#                         notifications_sent += 1
#                         current_notification_time += timedelta(minutes=interval_minutes)

#                         # Break if the next notification time exceeds noti_end_time
#                         if current_notification_time > noti_end_time:
#                             break

#                     except Exception as e:
#                         tb = traceback.format_exc()
#                         print(f"Error: {e}")
#                         errors.append(tb)

#         # Return response with success and error messages
#         if errors:
#             return Response({'error': errors, 'success': success}, status=status.HTTP_200_OK)
#         else:
#             return Response({'success': success}, status=status.HTTP_200_OK)

class check_and_notify_all_users(APIView):
    
    def get(self, request):
        current_time = timezone.now()
        errors = []
        success = []
        
        slot_details = SlotDetails.objects.all().values('site_id', 'designation_id')
        site_ids = [slot['site_id'] for slot in slot_details]
        designation_ids = [slot['designation_id'] for slot in slot_details]

        # Step 2: Get employee IDs based on site and designation IDs
        employee_ids = set(
            employee_site.objects.filter(site_id__in=site_ids).values_list('employee_id', flat=True)
        ).intersection(
            employee_designation.objects.filter(designation_id__in=designation_ids).values_list('employee_id', flat=True)
        )

        # Step 3: Fetch employees based on employee IDs to get phone numbers
        employees = sc_employee_master.objects.filter(employee_id__in=employee_ids)
        employee_phone_map = {emp.employee_id: emp.mobile_no for emp in employees}

        # Step 4: Iterate over employees and send notifications
        for employee_id, phone_number in employee_phone_map.items():
            # Retrieve CustomUser by phone number
            user = CustomUser.objects.filter(phone=phone_number).first()
            if not user:
                continue

            if user.phone != '8291104778':
                continue

            # Fetch slot IDs for the user's designation and site
            relevant_slot_ids = SlotDetails.objects.filter(
                designation_id__in=designation_ids, site_id__in=site_ids,shift_date__gte=current_time
            ).values_list('slot_id', flat=True)

            # Step 5: Fetch notification settings for each relevant slot ID
            notification_settings = SettingMaster.objects.filter(slot_id__in=relevant_slot_ids).values(
                'slot_id', 'noti_start_time', 'noti_end_time', 'interval', 'no_of_notification'
            )

            for setting in notification_settings:
                slot_id = setting['slot_id']
                noti_start_time = setting['noti_start_time']
                noti_end_time = setting['noti_end_time']
                interval_hours = int(setting['interval'])  # Interval in hours
                no_of_notification = int(setting['no_of_notification'])

                current_notification_time = noti_start_time
                notifications_sent = 0

                # Send the first notification immediately
                while notifications_sent < no_of_notification and current_notification_time <= noti_end_time:
                    try:
                        # Serialize shift data for notification
                        slot_instance = get_object_or_404(SlotDetails, slot_id=slot_id)
                        shift_data = SlotDetailsSerializer(slot_instance).data

                        # Log the notification in user_notification_log
                        notification_entry = user_notification_log.objects.create(
                            slot_id=slot_instance,
                            noti_send_time=timezone.now(),
                            notification_message="Notification for shift confirmation",
                            type_id=11,  # Replace with actual type_id if needed
                            created_by=user,
                            employee_id=employee_id,
                            emp_id=get_object_or_404(sc_employee_master, employee_id=employee_id)
                        )

                        # Send push notification
                        result = send_push_notification(user, shift_data, notification_entry.id)
                        if result != "success":
                            # Handle errors in sending notification
                            response_message = result.split("--")
                            if len(response_message) == 2:
                                error_detail = response_message[1]
                                if error_detail == "Requested entity was not found.":
                                    notification_entry.notification_message = "App Is Not Installed"
                                elif error_detail == "The registration token is not a valid FCM registration token":
                                    notification_entry.notification_message = "User Not Correctly Registered to the App. Please Login Again."
                                else:
                                    notification_entry.notification_message = result
                            else:
                                notification_entry.notification_message = result

                            notification_entry.save()
                            errors.append(f"Error sending notification to {user.full_name} - {result}")
                        else:
                            notification_entry.noti_receive_time = timezone.now()
                            notification_entry.save()

                        # Increment notification count and next notification time by interval hours
                        notifications_sent += 1
                        current_notification_time += timedelta(hours=interval_hours)

                        # Break if the next notification time exceeds noti_end_time
                        if current_notification_time > noti_end_time:
                            break

                    except Exception as e:
                        tb = traceback.format_exc()
                        print(f"Error: {e}")
                        errors.append(tb)

                

        # Return response with success and error messages
        if errors:
            return Response({'error': errors, 'success': success}, status=status.HTTP_200_OK)
        else:
            return Response({'success': success}, status=status.HTTP_200_OK)


        


class check_and_notify_default_users(APIView):
    def get(self, request):
        errors=[]
        success=[]
# 1. Filter sc_roster records based on the provided conditions
        roster_records = sc_roster.objects.filter(
            attendance_date__isnull=False,
            confirmation=True,
            attendance_in__isnull=True
        )

        # 2. Get employee_ids from the filtered sc_roster records
        employee_ids = roster_records.values_list('employee_id', flat=True)

        # 3. Find matching employees in sc_employee_master using employee_id
        matching_employees = sc_employee_master.objects.filter(employee_id__in=employee_ids)

        # # 4. Get the mobile numbers of the matched employees
        # employee_phones = matching_employees.values_list('mobile_no', flat=True)

        # # 5. Find matching CustomUser records using mobile_no (phone field)
        # matching_users = CustomUser.objects.filter(phone__in=employee_phones)

        # 6. Loop through matching employees and process all roster records for each employee
        for employee in matching_employees:
            # Get all roster records for the current employee
            employee_roster_records = roster_records.filter(employee_id=employee.employee_id)

            # Find the corresponding CustomUser (based on phone number)
            user = CustomUser.objects.filter(phone=employee.mobile_no).first()

            # If the user is found, process each roster record for this employee
            if user:
                for shift in employee_roster_records:
                    # Send each roster record and user to the function
                    serializer = SlotDetailsSerializer(shift)
                    shift_data = serializer.data
                    parameter_type = parameter_master.objects.get(parameter_id=13)
                    current_time = timezone.now()
                    
                    notification_entry = notification_log.objects.create(
                        sc_roster_id=shift,
                        notification_sent=current_time,
                        notification_message="Defaulter Notice!!!",
                        created_at=current_time,
                        type=parameter_type ,
                        created_by=user,  # assuming the current user is the creator
                        updated_at=current_time,
                        updated_by=user  # assuming the current user is the updater
                    )
                    notification_log_id = notification_entry.id
                    a = send_push_notification(user,shift_data,notification_log_id)
                    if(a!= "success"):
                        c = a.split("--")
                        if(len(c) == 2):
                            if(c[1] == "Requested entity was not found."):
                                notification_entry.notification_message = "App Is Not Installed"  # Update with the error message
                                notification_entry.save()     
                            elif(c[1] == "The registration token is not a valid FCM registration token")  :
                                notification_entry.notification_message = "User Not Correctly Registered to the App. Please Login Again."  # Update with the error message
                                notification_entry.save()     
                                
                            
                        else:
                            notification_entry.notification_message = a  # Update with the error message
                            notification_entry.save()
                        errors.append(f"Error sending notification to {user.full_name} - {a}")
                    else :
                        notification_entry.notification_received = timezone.now()
                        notification_entry.save()
                        success.append(f"successfully sent notification to {user.full_name} - {a}")
                    # process_notification(user, roster_record)
            
                    

def send_push_notification(user,shift_data,notification_log_id):
    try:
        
        # Retrieve and decode the base64-encoded credentials
        credentials_base64 = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_BASE64')
        if not credentials_base64:
            raise ValueError("GOOGLE_APPLICATION_CREDENTIALS_BASE64 environment variable is not set")

        credentials_json = base64.b64decode(credentials_base64).decode('utf-8')
        credentials_dict = json.loads(credentials_json)

        # Create credentials object
        SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']
        
        credentials = service_account.Credentials.from_service_account_info(credentials_dict,scopes=SCOPES)

        # Now use credentials as needed
        request = Request()
        credentials.refresh(request)
        access_token = credentials.token
        user_device_token = user.device_token

        print("Credentials have been set up successfully.")
        # SERVICE_ACCOUNT_FILE="./service-account-file.json"
        # SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']
        
        # credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE,scopes=SCOPES)
        # request = google.auth.transport.requests.Request()
        # credentials.refresh(request)
        # access_token = credentials.token
        # # The Firebase device token for the user. This should be saved in your user model or a related model.
        # user_device_token = user.device_token  # Assuming you have this field
        if not user_device_token:
            print("No device token found for user.")
            return  f"error sending no device for user"
        serialized_shift_data = json.dumps(shift_data)
        # Construct the notification payload
        payload = {
            "message":{
                'token': user_device_token,
                'notification': {
                    'title': 'Upcoming Shift Reminder',
                    'body': 'You have a shift scheduled for tomorrow.',
                    # "click_action": "FLUTTER_NOTIFICATION_CLICK"
                    # 'click_action': 'FLUTTER_NOTIFICATION_CLICK',
                    # 'sound': 'default'
                },
                'data': {
                    'title': 'Upcoming Shift Reminder',
                    'body': 'You have a shift scheduled for tomorrow.',
                    'type': 'shift_reminder',
                    'shift_data':serialized_shift_data,
                    'notification_log_id':str(notification_log_id),
                }
                
            }
        }
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        # Send the request to FCM
        response = requests.post('https://fcm.googleapis.com/v1/projects/appnotification-85128/messages:send', json=payload, headers=headers)
        if response.status_code == 200:
            print("Notification sent successfully.")
            return "success"
        else:
            response_data = json.loads(response.text)
            message = response_data.get('error', {}).get('message', '')
            print(f"Failed to send notification. Status Code: {response.status_code}, Response: {message}")
            return f"error sending {response.status_code}--{message}"
            
    except Exception as e:
        print(str(e))
        return f"error sending {str(e)}--{str(e)}"

def process_notification(user, roster_record):
    print(1)
    # Example: processing each roster record and sending notification
    # send_notification(user, f"Attendance reminder for employee: {roster_record.employee_id} on date: {roster_record.shift_date}")

# class DefaultRecords(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]

#     def get(self, request):
#         try:
#             # Step 1: Extract user from JWT token
#             user = request.user  # This gets the user from the JWT token if authenticated

#             # Step 2: Fetch the corresponding user from the CustomUser model
#             custom_user = get_object_or_404(CustomUser, id=user.id)

#             # Step 3: Fetch the employee_id from sc_employee_master using custom_user
#             try:
#                 employee_record = sc_employee_master.objects.filter(mobile_no=custom_user.phone).first()
#             except sc_employee_master.DoesNotExist:
#                 return Response(
#                     {"error": "Employee record not found for the current user."},
#                     status=status.HTTP_404_NOT_FOUND
#                 )

#             # Step 4: Using the employee_id, fetch the sc_roster records with specified conditions
#             employee_id = employee_record.employee_id
#             roster_records = sc_roster.objects.filter(
#                 employee_id=employee_id,
#                 attendance_date__isnull=False,  # attendance_date is not null
#                 confirmation=True,  # confirmation is true
#                 attendance_in__isnull=True  # attendance_in is null
#             )

#             # Step 5: Check if roster_records exist
#             if not roster_records.exists():
#                 return Response(
#                     {"message": "No matching sc_roster records found for the employee."},
#                     status=status.HTTP_404_NOT_FOUND
#                 )

#             # Step 6: Serialize the data
#             data = ScRosterSerializer(roster_records, many=True)

#             # Step 7: Return a success response
#             return Response(data.data, status=status.HTTP_200_OK)

#         except Exception as e:
#             # Step 8: Return a generic error response for any unhandled exceptions
#             return Response(
#                 {"error": f"An error occurred: {str(e)}"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

# class DefaultRecords(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]

#     def get(self, request):
#         try:
#             # Step 1: Extract user from JWT token
#             user = request.user  # This gets the user from the JWT token if authenticated

#             # Step 2: Fetch the corresponding user from the CustomUser model
#             custom_user = get_object_or_404(CustomUser, id=user.id)

#             # Step 3: Fetch the employee_id from sc_employee_master using custom_user
#             try:
#                 employee_record = sc_employee_master.objects.filter(mobile_no=custom_user.phone).first()
#             except sc_employee_master.DoesNotExist:
#                 return Response(
#                     {"error": "Employee record not found for the current user."},
#                     status=status.HTTP_404_NOT_FOUND
#                 )

#             # Step 4: Using the employee_id, fetch UserSlotDetails records
#             employee_id = employee_record.employee_id
#             user_slot_details = UserSlotDetails.objects.filter(employee_id=employee_id)

#             # Step 5: Check if UserSlotDetails exist
#             if not user_slot_details.exists():
#                 return Response(
#                     {"message": "No matching UserSlotDetails records found for the employee."},
#                     status=status.HTTP_404_NOT_FOUND
#                 )

#             # Step 6: Filter UserSlotDetails records where corresponding data does not exist in UserAttendanceDetails
#             filtered_data = []
#             for slot in user_slot_details:
#                 slot_id = slot.slot_id
#                 # Check if there is no entry in UserAttendanceDetails for this employee_id and slot_id
#                 attendance_exists = slot_attendance_details.objects.filter(
#                     employee_id=employee_id,
#                     slot_id=slot_id
#                 ).exists()

#                 if not attendance_exists:
#                     filtered_data.append(slot)

#             # Step 7: If no matching data, return not found message
#             if not filtered_data:
#                 return Response(
#                     {"message": "No UserSlotDetails records found without corresponding attendance details."},
#                     status=status.HTTP_404_NOT_FOUND
#                 )

#             # Step 8: Serialize the filtered UserSlotDetails data
#             data = UserSlotDetailsSerializer1(filtered_data, many=True)

#             # Step 9: Return a success response with the serialized data
#             return Response(data.data, status=status.HTTP_200_OK)

#         except Exception as e:
#             # Step 10: Return a generic error response for any unhandled exceptions
#             return Response(
#                 {"error": f"An error occurred: {str(e)}"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

class DefaultRecords(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            # Step 1: Extract user from JWT token
            user = request.user  # This gets the user from the JWT token if authenticated

            # Step 2: Fetch the corresponding user from the CustomUser model
            custom_user = get_object_or_404(CustomUser, id=user.id)

            # Step 3: Fetch the employee_id from sc_employee_master using custom_user
            try:
                employee_record = sc_employee_master.objects.filter(mobile_no=custom_user.phone).first()
            except sc_employee_master.DoesNotExist:
                return Response(
                    {"error": "Employee record not found for the current user."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Step 4: Using the employee_id, fetch UserSlotDetails records
            employee_id = employee_record.employee_id
            user_slot_details = UserSlotDetails.objects.filter(employee_id=employee_id)

            # Step 5: Check if UserSlotDetails exist
            if not user_slot_details.exists():
                return Response(
                    {"message": "No matching UserSlotDetails records found for the employee."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Step 6: Create a list to hold the serialized results with attendance check
            results = []
            serialized_data = UserSlotDetailsSerializer1(user_slot_details, many=True)

            # Step 7: Check for attendance in UserAttendanceDetails for each UserSlotDetails record
            for index, slot in enumerate(user_slot_details):
                slot_id = slot.slot_id
                # Check if there is no entry in UserAttendanceDetails for this employee_id and slot_id
                attendance_exists = slot_attendance_details.objects.filter(
                    employee_id=employee_id,
                    slot_id=slot_id
                ).exists()

                # Append the attendance check result (1 or 0)
                serialized_data.data[index]['attendance_check'] = 1 if not attendance_exists else 0

            # Step 8: Return the results with both serialized data and attendance check
            return Response(serialized_data.data, status=status.HTTP_200_OK)

        except Exception as e:
            # Step 9: Return a generic error response for any unhandled exceptions
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




