"""
URL configuration for PSNHeadon project.

The `urlpatterns` list routes URLs to  For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', Account, name='Account')
Class-based views
    1. Add an import:  from other_app.views import Account
    2. Add a URL to urlpatterns:  path('', Account.as_view(), name='Account')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from Account.views import *
from Dashboard.views import *
# from Masters.models import site_master
from Masters.views import *
from Payroll.views import *
from Reports.views import *
from Masters.views import site_master as sm
from Masters.views import company_master as cm
from django.urls import path
from Notification.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # APP URLS
    path('refresh-token', CustomTokenRefreshView.as_view(), name='refresh-token'),
    path('Applogin', LoginView.as_view(), name='Applogin'),
    path('register_device_token', register_device_token.as_view(), name='register_device_token'),
    path("register",RegistrationView.as_view(),name='register'),
    path('home_fetch', RosterDataAPIView.as_view(), name='home_fetch'),
    path('home_fetch', SlotDataAPIView.as_view(), name='home_fetch'),
    path('employee_data', EmployeeData.as_view(), name='employee_data'),
    path('confirm_schedule', confirm_schedule.as_view(), name='confirm_schedule'),
    path('confirm_notification', confirm_notification.as_view(), name='confirm_notification'),
    path('check_and_notify_user', check_and_notify_user.as_view(), name='check_and_notify_user'),
    path('check_and_notify_all_users', check_and_notify_all_users.as_view(), name='check_and_notify_all_users'),
    path('check_and_notify_default_users', check_and_notify_default_users.as_view(), name='check_and_notify_default_users'),
    path('DefaultRecords', DefaultRecords.as_view(), name='DefaultRecords'),
    
    # Dashboard
    path("newdashboard",newdashboard,name='newdashboard'),
    path("get_sites",get_sites,name='get_sites'),
    path("updateGraph",updateGraph, name="updateGraph"),
    path("get_roster_data",get_roster_data, name="get_roster_data"),
    path("get_roster_data_tommorow",get_roster_data_tommorow, name="get_roster_data_tommorow"),

    # Account

    path("", Login,name='Account'),
    path("Login", Login,name='Login'),
    path("home", home,name='home'),
    path("logout",logoutView,name='logout'),
    path("forgot_password",forgot_password,name='forgot_password'),
    path('search/', search, name='search'),
    path("register_new_user",register_new_user, name="register_new_user"),
    path("reset_password",reset_password, name="reset_password"),
    path("change_password",change_password, name="change_password"),
    path("forget_password_change",forget_password_change, name="forget_password_change"),

    # Masters
    path('masters/', masters, name='masters'),
    path('sample_xlsx/', sample_xlsx, name='sample_xlsx'),
    path("roster_upload",roster_upload, name="roster_upload"),
    path("company_master",cm,name="company_master"),
    path("employee_master",employee_master, name="employee_master"),
    path("upload_excel",upload_excel, name="upload_excel"),
    path("site_master",sm, name="site_master"),
    path("designation_master1",designation_master1, name="designation_master1"),
    path("get_access_control",get_access_control, name="get_access_control"),
    path("slot_details",slot_details, name="slot_details"),
    path("post_slot_details",post_slot_details, name="post_slot_details"),
    path("setting_master",setting_master, name="setting_master"),
    path("edit_slot_details",edit_slot_details, name="edit_slot_details"),
    path("delete_slot",delete_slot, name="delete_slot"),
    path("view_employee",view_employee, name="view_employee"),
    path("view_designation",view_designation, name="view_designation"),
    path("employee_upload",employee_upload, name="employee_upload"),
    path("deactivate_slot",deactivate_slot, name="deactivate_slot"),
    path("designation_master1",designation_master1, name="designation_master1"),
    # path("view_employee",view_employee, name="view_employee"),
    path("view_designation",view_designation, name="view_designation"),
    path('EmployeeData', EmployeeData.as_view(), name='EmployeeData'),
    path('StateName', StateName.as_view(), name='StateName'),

    #Reports 
    path('common_html', common_html, name='common_html'),
    path('get_filter', get_filter, name='get_filter'),
    path('get_sub_filter', get_sub_filter, name='get_sub_filter'),
    path('add_new_filter', add_new_filter, name='add_new_filter'),
    path('partial_report', partial_report, name='partial_report'),
    path('report_pdf', report_pdf, name='report_pdf'),
    path('report_xlsx', report_xlsx, name='report_xlsx'),
    path('save_filters', save_filters, name='save_filters'),
    path('delete_filters', delete_filters, name='delete_filters'),
    path('saved_filters', saved_filters, name='saved_filters'),
    
    # Menu Management
    path("menu_admin",menu_admin, name="menu_admin"),
    path("menu_master",menu_master, name="menu_master"),
    path("assign_menu",assign_menu, name="assign_menu"),
    path("get_assigned_values",get_assigned_values, name="get_assigned_values"),
    path("menu_order",menu_order, name="menu_order"),
    path("delete_menu",delete_menu, name="delete_menu"),
    
    # Bootstarp Pages
    path("dashboard",dashboard,name='dashboard'),
    path("buttons",buttons,name='buttons'),
    path("cards",cards,name='cards'),
    path("utilities_color",utilities_color,name='utilities_color'),
    path("utilities_border",utilities_border,name='utilities_border'),
    path("utilities_animation",utilities_animation,name='utilities_animation'),
    path("utilities_other",utilities_other,name='utilities_other'),
    path("error_page",error_page,name='error_page'),
    path("blank",blank,name='blank'),
    path("charts",charts,name='charts'),  
    path("tables",tables,name='tables'),

    #payroll
    
    path('salary_element_index', index, name='salary_element_index'),
    path('salary_element_create/', create, name='salary_element_create'),
    path('salary_element_edit/<int:pk>/', edit, name='salary_element_edit'),
    path('salary_element_view/<int:pk>/', view, name='salary_element_view'),
    path('rate_card_index', rate_card_index, name='rate_card_index'),
    path('rate-card/create/', rate_card_create, name='rate_card_create'),
    path('rate-card/<int:card_id>/edit/', rate_card_edit, name='rate_card_edit'),
    path('rate-card/<int:card_id>/view/', rate_card_view, name='rate_card_view'),
    path('site_card_relation_index', site_card_relation_index, name='site_card_relation_index'),
    path('site_card_relation/create/', site_card_relation_create, name='site_card_relation_create'),
    path('site_card_relation/edit/<int:pk>/', site_card_relation_edit, name='site_card_relation_edit'),
    path('site_card_relation/view/<int:pk>/', site_card_relation_view, name='site_card_relation_view'),
    # path('check_shift/<int:employee_id>/<int:site_id>/', check_shift_for_next_day, name='check_shift_for_next_day'),
    path('get_rate_cards/<int:site_id>/', get_rate_cards, name='get_rate_cards'),
    path('employee_rate_card_create', employee_rate_card_create, name='employee_rate_card_create'),
    path('employee_rate_card_edit/<int:id>/', employee_rate_card_edit, name='employee_rate_card_edit'),
    path('employee_rate_card_view/<int:id>/', employee_rate_card_view, name='employee_rate_card_view'),
    path('employee_rate_card_index', employee_rate_card_index, name='employee_rate_card_index'),
    path('employee_rate_card_create/', employee_rate_card_create, name='employee_rate_card_create'),
    
    path('slots', SlotListView.as_view(), name='slot_list'),
    path('slots/<int:slot_id>/', user_slot_details_list, name='user_slot_details_list'),
    path('slots/generate-salary/<int:slot_id>/', generate_salary_redirect, name='generate_salary_redirect'),
    path('calculate-salary/<int:slot_id>/', calculate_daily_salary, name='generate_salary'),
    
    path('attendance_index', attendance_index, name='attendance_index'),
    
    path('attendance/create', upload_attendance, name='create_attendance'),
    path('get_sites', get_sites, name='get_sites'),
    path('get_slots', get_slots, name='get_slots'),

]