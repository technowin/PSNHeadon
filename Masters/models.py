from django.db import models

# Create your models here.

from django.db import models

from Account.models import CustomUser
from Payroll.models import StatusMaster, designation_master


     
class Roles(models.Model):
    id = models.AutoField(primary_key=True)
    role_id = models.IntegerField(null=True, blank=False)
    role_name = models.TextField(null=True, blank=True)
    role_type = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    created_by = models.ForeignKey('Account.CustomUser', on_delete=models.CASCADE, related_name='roles_created', blank=True, null=True, db_column='created_by')
    updated_by = models.ForeignKey('Account.CustomUser', on_delete=models.CASCADE, related_name='roles_updated', blank=True, null=True, db_column='updated_by')
    class Meta:
        db_table = 'roles'



# Create your models here.
class company_master(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.TextField(null=True,blank=True)
    company_address =models.TextField(null=True,blank=True)
    pincode =models.TextField(null=True,blank=True)
    contact_person_name =models.TextField(null=True,blank=True)
    contact_person_email =models.TextField(null=True,blank=True)
    contact_person_mobile_no =models.TextField(null=True,blank=True)
    is_active =models.BooleanField(null=True,blank=True,default=True)
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='company_created_by',blank=True, null=True,db_column='created_by')
    updated_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='company_updated_by',blank=True, null=True,db_column='updated_by')
    class Meta:
        db_table = 'company_master'
    def __str__(self):
        return self.company_name



class parameter_master(models.Model):
    parameter_id = models.AutoField(primary_key=True)
    parameter_name =models.TextField(null=True,blank=True)
    parameter_value =models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='parameter_created_by',blank=True, null=True,db_column='created_by')
    updated_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='parameter_updated_by',blank=True, null=True,db_column='updated_by')
    class Meta:
        db_table = 'parameter_master'
    def __str__(self):
        return self.parameter_value
    
class StateMaster(models.Model):
    state_id =  models.AutoField(primary_key=True)
    state_name = models.TextField(null=True,blank=True) 
    state_status = models.BooleanField(null=True,blank=True,default=True)
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='state_created',blank=True, null=True,db_column='created_by')
    updated_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='state_updated',blank=True, null=True,db_column='updated_by')
    class Meta:
        db_table = 'tbl_state_master'
    def __str__(self):
        return self.state_name
class CityMaster(models.Model):
    id =  models.AutoField(primary_key=True)
    city_id =  models.IntegerField(null=True, blank=False)
    city_name = models.TextField(null=True,blank=True) 
    city_status = models.BooleanField(null=True,blank=True,default=True)
    state = models.ForeignKey(StateMaster, on_delete=models.CASCADE,related_name='state_city_id',blank=True, null=True,db_column='state_id')
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='city_created',blank=True, null=True,db_column='created_by')
    updated_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='city_updated',blank=True, null=True,db_column='updated_by')
    class Meta:
        db_table = 'tbl_city_master'
    def __str__(self):
        return self.city_name       


class site_master(models.Model):
    site_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(company_master, on_delete=models.CASCADE,related_name='company_relation',blank=True, null=True)
    state_id = models.ForeignKey(StateMaster, on_delete=models.CASCADE,related_name='state_master_site_master',blank=True, null=True,db_column="state_id")
    city_id = models.ForeignKey(CityMaster, on_delete=models.CASCADE,related_name='city_master_city_id',blank=True, null=True,db_column="city_id")
    site_name =models.TextField(null=True,blank=True)
    site_address =models.TextField(null=True,blank=True)
    pincode =models.TextField(null=True,blank=True)
    contact_person_name =models.TextField(null=True,blank=True)
    contact_person_email =models.TextField(null=True,blank=True)
    contact_person_mobile_no =models.TextField(null=True,blank=True)
    is_active =models.BooleanField(null=True,blank=True,default=True)
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='site_created',blank=True, null=True,db_column='created_by')
    updated_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='site_updated',blank=True, null=True,db_column='updated_by')
    class Meta:
        db_table = 'site_master'
    def __str__(self):
        company_name = self.company.company_name if self.company else "No Company"
        return f"{company_name} - {self.site_name}" if self.site_name else company_name
    
class sc_employee_master(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id =models.TextField(null=True,blank=True)
    employee_name =models.TextField(null=True,blank=True)
    gender = models.TextField(null=True,blank=True)
    handicapped = models.BooleanField(null=True,blank=True,default=True)
    # state = models.IntegerField(null=True, blank=False)
    state_id = models.ForeignKey(StateMaster, on_delete=models.CASCADE,related_name='employee_relation_state_id',blank=True, null=True,db_column='state_id')
    city = models.TextField(null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    pincode  = models.TextField(null=True,blank=True)
    mobile_no =models.TextField(null=True,blank=True)
    email = models.TextField(null=True,blank=True)
    uan_no = models.TextField(null=True,blank=True)
    pf_no = models.TextField(null=True,blank=True)
    esic =  models.TextField(null=True,blank=True)
    bank_name = models.TextField(null=True,blank=True)
    branch_name = models.TextField(null=True,blank=True)
    ifsc_code =  models.TextField(null=True,blank=True)
    account_no =  models.TextField(null=True,blank=True)
    account_holder_name =  models.TextField(null=True,blank=True)
    company_id = models.ForeignKey(company_master, on_delete=models.CASCADE,related_name='employee_relation',blank=True, null=True,db_column='company_id')
    employment_status = models.ForeignKey(parameter_master, on_delete=models.CASCADE,related_name='parameter_data',blank=True, null=True)
    is_active =models.BooleanField(null=True,blank=True,default=True)
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='sc_employee_created',blank=True, null=True,db_column='created_by')
    updated_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='sc_employee_updated',blank=True, null=True,db_column='updated_by')
    class Meta:
        db_table = 'sc_employee_master'
    # def __str__(self):
    #     return self.employee_name
    
 
class application_search(models.Model):
    id = models.AutoField(primary_key=True)
    name =models.TextField(null=True,blank=True)
    description =models.TextField(null=True,blank=True)
    href =models.TextField(null=True,blank=True)
    menu_id =models.TextField(null=True,blank=True)
    is_active =models.BooleanField(null=True,blank=True,default=True)
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='app_search_created',blank=True, null=True,db_column='created_by')
    updated_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='app_search_updated',blank=True, null=True,db_column='updated_by')
    class Meta:
        db_table = 'application_search'
    def __str__(self):
        return self.name

class file_checksum(models.Model):
    checksum_id = models.AutoField(primary_key=True)
    upload_for =models.TextField(null=True,blank=True)
    company = models.ForeignKey(company_master, on_delete=models.CASCADE,related_name='checksum_company',blank=True, null=True)
    worksite =models.TextField(null=True,blank=True)
    month =models.TextField(null=True,blank=True)
    year =models.TextField(null=True,blank=True)
    file_name = models.TextField(null=True, blank=True)
    checksum_message = models.TextField(null=True, blank=True)
    status = models.TextField(null=True, blank=True)
    error_count = models.TextField(null=True, blank=True)
    update_count = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='checksum_created_by',blank=True, null=True,db_column='created_by')

    class Meta:
        db_table = 'file_checksum'


class file_errorlog(models.Model):
    error_id = models.AutoField(primary_key=True)
    upload_for =models.TextField(null=True,blank=True)
    company = models.ForeignKey(company_master, on_delete=models.CASCADE,related_name='errorlog_company',blank=True, null=True)
    worksite =models.TextField(null=True,blank=True)
    file_name = models.TextField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    checksum = models.ForeignKey(file_checksum, on_delete=models.CASCADE,related_name='checksum1_created_by',blank=True, null=True)
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='file_errorlog_created_by',blank=True, null=True,db_column='created_by')

    class Meta:
        db_table = 'file_errorlog'    
    
class sc_roster(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id =models.TextField(null=True,blank=True)
    employee_name =models.TextField(null=True,blank=True)
    company = models.ForeignKey(company_master, on_delete=models.CASCADE,related_name='roster_company',blank=True, null=True)
    worksite =models.TextField(null=True,blank=True)
    shift_date = models.DateField(null=True,blank=True)
    shift_time = models.TextField(null=True,blank=True)
    confirmation = models.BooleanField(null=True,blank=True,default=False)
    confirmation_date = models.DateTimeField(null=True,blank=True)
    attendance_in = models.TextField(null=True,blank=True)
    attendance_out = models.TextField(null=True,blank=True)
    attendance_date = models.DateTimeField(null=True,blank=True)
    checksum = models.ForeignKey(file_checksum, on_delete=models.CASCADE,related_name='checksum_roster',blank=True, null=True)
    uploaded_date = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='uploaded_by',blank=True, null=True,db_column='uploaded_by')
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='roster_created_by',blank=True, null=True,db_column='created_by')
    updated_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='roster_updated_by',blank=True, null=True,db_column='updated_by')
    class Meta:
        db_table = 'sc_roster'
    def __str__(self):
        return self.employee_id


        
class Log(models.Model):
    log_text = models.TextField(null=True,blank=True)
    class Meta:
        db_table = 'logs'

    
class SlotDetails(models.Model):
    slot_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(company_master, on_delete=models.CASCADE,related_name='slot_relation',blank=True, null=True)
    # worksite = models.TextField(null=True,blank=True)
    setting_id  = models.ForeignKey('Masters.SettingMaster', on_delete=models.CASCADE,related_name='SlotDetails_setting_id',blank=True, null=True,db_column="setting_id")
    site_id = models.ForeignKey(site_master, on_delete=models.CASCADE,related_name='SlotDetails_site_id',blank=True, null=True,db_column="site_id")
    designation_id = models.ForeignKey('Payroll.designation_master', on_delete=models.CASCADE,related_name='SlotDetails_designation_id',blank=True, null=True,db_column="designation_id")
    slot_name = models.TextField(null=True,blank=True)
    slot_description = models.CharField(max_length=200, null=True, blank=True)
    shift_date = models.DateField(null=True,blank=True)
    start_time = models.TextField(null=True,blank=True)
    end_time = models.TextField(null=True,blank=True)
    night_shift = models.BooleanField(null=True,blank=True,default=True)
    status = models.ForeignKey('Payroll.StatusMaster', on_delete=models.CASCADE,related_name='slot_status',blank=True, null=True,db_column='status_id')
    is_active =models.BooleanField(null=True,blank=True,default=True)
    message = models.TextField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='slot_created',blank=True, null=True,db_column='created_by')
    updated_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='slot_updated',blank=True, null=True,db_column='updated_by')
    class Meta:
        db_table = 'slot_details'
    def __str__(self):
        return self.slot_name



class SettingMaster(models.Model):
    id= models.AutoField(primary_key=True)
    slot_id = models.ForeignKey(SlotDetails, on_delete=models.CASCADE,related_name='setting_relation',blank=True, null=True,db_column='slot_id')
    noti_start_time =  models.DateField(null=True,blank=True)
    noti_end_time = models.DateField(null=True,blank=True)
    no_of_notification = models.IntegerField(null=True, blank=False)
    no_of_employee =  models.IntegerField(null=True, blank=False)
    interval = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='setting_created',blank=True, null=True,db_column='created_by')
    updated_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='setting_updated',blank=True, null=True,db_column='updated_by')
    class Meta:
        db_table = 'setting_master'
    def __str__(self):
        return self.name
    
class UserSlotDetails(models.Model):
    id = models.AutoField(primary_key=True) 
    emp_id =  models.ForeignKey(sc_employee_master, on_delete=models.CASCADE,related_name='UserSlotDetails_emp_id',blank=True, null=True,db_column='emp_id')
    employee_id = models.TextField(null=True,blank=True)
    company_id = models.ForeignKey(company_master, on_delete=models.CASCADE,related_name='UserSlotDetails_company_id',blank=True, null=True,db_column='company_id')
    site_id = models.ForeignKey(site_master, on_delete=models.CASCADE,related_name='UserSlotDetails_site_id',blank=True, null=True,db_column='site_id')
    slot_id = models.ForeignKey(SlotDetails, on_delete=models.CASCADE,related_name='UserSlotDetails_slot_id',blank=True, null=True,db_column='slot_id')
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE,related_name='UserSlotDetails_status_id',blank=True, null=True,db_column='status_id')
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='user_shit_created',blank=True, null=True,db_column='created_by') 
    class Meta:
        db_table = 'user_slot_details'
    
class employee_designation(models.Model):
    id =  models.AutoField(primary_key=True)
    designation_id = models.ForeignKey(designation_master, on_delete=models.CASCADE,related_name='employee_designation_relation',blank=True, null=True,db_column='designation_id')
    company_id= models.ForeignKey(company_master, on_delete=models.CASCADE,related_name='comapny_designation_relation',blank=True, null=True,db_column='company_id')
    employee_id = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'employee_designation'
    def __str__(self):
        return self.name
    

class employee_site(models.Model):
    id =  models.AutoField(primary_key=True)
    site_id = models.ForeignKey(site_master, on_delete=models.CASCADE,related_name='employee_site_relation',blank=True, null=True,db_column='site_id')
    company_id= models.ForeignKey(company_master, on_delete=models.CASCADE,related_name='comapny_site_relation',blank=True, null=True,db_column='company_id')
    employee_id =models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'employee_site'
    def __str__(self):
        return self.name
    

class HistUserSlotDetails(models.Model):
    id = models.AutoField(primary_key=True) 
    emp_id =  models.ForeignKey(sc_employee_master, on_delete=models.CASCADE,related_name='HistUserSlotDetails_emp_id',blank=True, null=True,db_column='emp_id')
    employee_id = models.TextField(null=True,blank=True)
    company_id = models.ForeignKey(company_master, on_delete=models.CASCADE,related_name='HistUserSlotDetails_company_id',blank=True, null=True,db_column='company_id')
    site_id = models.ForeignKey(site_master, on_delete=models.CASCADE,related_name='HistUserSlotDetails_site_id',blank=True, null=True,db_column='site_id')
    slot_id = models.ForeignKey(SlotDetails, on_delete=models.CASCADE,related_name='HistUserSlotDetails_slot_id',blank=True, null=True,db_column='slot_id')
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='Hist_user_shit_created',blank=True, null=True,db_column='created_by') 
    class Meta:
        db_table = 'hist_user_slot_details'
    def __str__(self):
        return self.name
    