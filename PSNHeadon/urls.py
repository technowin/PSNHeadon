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
from Menu.views import *
from Payroll.views import *
from Reports.views import *
from Masters.views import site_master as sm
from Masters.views import company_master as cm
from django.urls import path
from Notification.views import *
from Tax.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # APP URLS
    path('refresh-token', CustomTokenRefreshView.as_view(), name='refresh-token'),
    path('Applogin', LoginView.as_view(), name='Applogin'),
    path('register_device_token', register_device_token.as_view(), name='register_device_token'),
    path("register",RegistrationView.as_view(),name='register'),
    path('home_slot_fetch', SlotDataAPIView.as_view(), name='home_slot_fetch'),
    path('employee_data', EmployeeData.as_view(), name='employee_data'),
    path('confirm_schedule', confirm_schedule.as_view(), name='confirm_schedule'),
    path('confirm_notification', confirm_notification.as_view(), name='confirm_notification'),
    path('check_and_notify_user', check_and_notify_user.as_view(), name='check_and_notify_user'),
    path('check_and_notify_all_users', check_and_notify_all_users.as_view(), name='check_and_notify_all_users'),
    path('check_and_notify_default_users', check_and_notify_default_users.as_view(), name='check_and_notify_default_users'),
    path('post_user_slot', post_user_slot.as_view(), name='post_user_slot'),
    path('delete_user_slot', delete_user_slot.as_view(), name='delete_user_slot'),
    path('DefaultRecords', DefaultRecords.as_view(), name='DefaultRecords'),
    path('EmployeeData', EmployeeData.as_view(), name='EmployeeData'),
    path('StateName', StateName.as_view(), name='StateName'),
    path('send_reminder_notifications', send_reminder_notifications.as_view(), name='send_reminder_notifications'),
    path('update_bank_details', update_bank_details.as_view(), name='update_bank_details'),
    path('payment_details', payment_details.as_view(), name='payment_details'),
    path('payment_slip_details', payment_slip_details.as_view(), name='payment_slip_details'),
    path('show_notification', show_notification.as_view(), name='show_notification'),
    path('save_notification', save_notification.as_view(), name='save_notification'),
    
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
    path('upload_excel_cm', upload_excel_cm, name='upload_excel_cm'),
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
    path("worksite_upload",worksite_upload, name="employee_upload"),
    path("deactivate_slot",deactivate_slot, name="deactivate_slot"),
    path("designation_master1",designation_master1, name="designation_master1"),
    # path("view_employee",view_employee, name="view_employee"),
    path("view_designation",view_designation, name="view_designation"),
    path("get_worksites",get_worksites, name="get_worksites"),
    path("check_slot_name",check_slot_name, name="check_slot_name"),
    path('fetch-cities/', fetch_cities, name='fetch_cities'),
    # path("update_remaining_companies",update_remaining_companies, name="update_remaining_companies"),
    

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
    path('salary_element_edit/<str:pk>/', edit, name='salary_element_edit'),
    path('salary_element_view/<str:pk>/', view, name='salary_element_view'),
    path('rate_card_index', rate_card_index, name='rate_card_index'),
    path('rate-card/create/', rate_card_create, name='rate_card_create'),
    path('rate-card/<str:card_id>/edit/', rate_card_edit, name='rate_card_edit'),
    path('rate-card/<str:card_id>/view/', rate_card_view, name='rate_card_view'),
    path('site_card_relation_index', site_card_relation_index, name='site_card_relation_index'),
    path('site_card_relation/create/', site_card_relation_create, name='site_card_relation_create'),
    path('site_card_relation/edit/<str:pk>/', site_card_relation_edit, name='site_card_relation_edit'),
    path('site_card_relation/view/<str:pk>/', site_card_relation_view, name='site_card_relation_view'),
    # path('check_shift/<int:employee_id>/<int:site_id>/', check_shift_for_next_day, name='check_shift_for_next_day'),
    path('get_rate_cards/<int:site_id>/', get_rate_cards, name='get_rate_cards'),
    path('employee_rate_card_create', employee_rate_card_create, name='employee_rate_card_create'),
    path('employee_rate_card_edit/<int:id>/', employee_rate_card_edit, name='employee_rate_card_edit'),
    path('employee_rate_card_view/<int:id>/', employee_rate_card_view, name='employee_rate_card_view'),
    path('employee_rate_card_index', employee_rate_card_index, name='employee_rate_card_index'),
    path('employee_rate_card_create/', employee_rate_card_create, name='employee_rate_card_create'),
    
    path('slots', SlotListView.as_view(), name='slot_list'),
    path('slots', SlotListView.as_view(), name='slot_list'),
    path('approveslots', ApproveSlotListView.as_view(), name='approveslots'),
    path('update_payout_status', UpdatePayoutStatus.as_view(), name='update_payout_status'),

    path('user_salary_index', user_salary_index, name='user_salary_index'),
    path('view_approve_salary/<int:slot_id>', view_approve_salary, name='view_approve_salary'),
    path('edit_attendance/<str:encrypted_id>', edit_attendance, name='edit_attendance'),
    path('employee/<str:employee_id>/slot/<int:slot_id>/salary-details/', view_employee_salary_details, name='view_employee_salary_details'),
    path('slots/<int:slot_id>/', user_slot_details_list, name='user_slot_details_list'),
    path('slots/generate-salary/<int:slot_id>/', generate_salary_redirect, name='generate_salary_redirect'),
    path('calculate-salary/<int:slot_id>/', calculate_daily_salary, name='generate_salary'),
    
    path('attendance_index', attendance_index, name='attendance_index'),
    
    path('attendance/create', upload_attendance, name='create_attendance'),
    path('attendance/approve', approve_attendance, name='approve_attendance'),
    path('get_sites', get_sites, name='get_sites'),
    path('get_slots', get_slots, name='get_slots'),
    path('handle_card_name_change', handle_card_name_change, name='handle_card_name_change'),
    path('download_sample/', download_sample, name='download_sample'),
    path('attendance_error/', attendance_error, name='attendance_error'),

    path('create_payout', create_payout, name='create_payout'),
    path('create_new_payout/<str:employee_id>/slot/<int:slot_id>', create_new_payout, name='create_new_payout'),
    path('generate_pay_slip', generate_pay_slip, name='generate_pay_slip'),
    path('refresh_payout_status', refresh_payout_status, name='refresh_payout_status'),


    #TAX

    path('state_master_index', state_master_index, name='state_master_index'),
    path('state_edit/<str:pk>/', state_edit, name='state_edit'),
    path('state_view/<str:pk>/', state_view, name='state_view'),
    path('state_create', state_create, name='state_create'),

    path('city_master_index/<str:pk>/', city_master_index, name='city_master_index'),
    path('city_edit/<str:pk>', city_edit, name='city_edit'),
    path('city_view/<str:pk>', city_view, name='city_view'),
    path('city_create/<str:state_id>/', city_create, name='city_create'),

    path('act_master_index', act_master_index, name='act_master_index'),
    path('act_edit/<str:pk>/', act_edit, name='act_edit'),
    path('act_view/<str:pk>/', act_view, name='act_view'),
    path('act_create', act_create, name='act_create'),

    path('slab_index/<str:pk>/', slab_index, name='slab_index'),
    path('slab_edit/<str:pk>/', slab_edit, name='slab_edit'),
    path('slab_view/<str:pk>/', slab_view, name='slab_view'),
    path('slab_create', slab_create, name='slab_create'),

    path('slab_master_index', slab_master_index, name='slab_master_index'),
    path('slab_master_edit/<str:pk>/', slab_master_edit, name='slab_master_edit'),
    path('slab_master_view/<str:pk>/', slab_master_view, name='slab_master_view'),
    path('slab_master_create', slab_master_create, name='slab_master_create'),
    path('check_slab_combination', check_slab_combination, name='check_slab_combination'),

    path('income_tax_master_index', income_tax_master_index, name='income_tax_master_index'),
    path('income_tax_edit/<str:pk>/', income_tax_edit, name='income_tax_edit'),
    path('income_tax_view/<str:pk>/', income_tax_view, name='income_tax_view'),
    path('income_tax_create', income_tax_create, name='income_tax_create'),

]