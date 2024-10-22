from django.db import models

from Account.models import CustomUser
# from Masters.models import site_master

# from Masters.models import company_master, site_master,SlotDetails
# from Masters.views import slot_details

# Create your models here.
class salary_element_master(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.TextField(null=True,blank=True)
    pay_type = models.TextField(null=True,blank=True)
    classification = models.TextField(null=True,blank=True)
    
    is_active =models.BooleanField(null=True,blank=True,default=True)
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='salary_item_created_by',blank=True, null=True,db_column='created_by')
    updated_at = models.DateTimeField(null=True,blank=True,auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='salary_item_updated_by',blank=True, null=True,db_column='updated_by')
    class Meta:
        db_table = 'salary_element_master'
    def __str__(self):
        return f"{self.item_name} - {self.pay_type} - {self.classification}"
    
class rate_card_master(models.Model):
    card_id = models.AutoField(primary_key=True)
    card_name = models.TextField(null=True, blank=True)
    
    # Use a through model to store extra information for each salary element
    # item_id = models.ManyToManyField(salary_element_master, through='RateCardSalaryElement', related_name='rate_cards', blank=True)
    item_ids = models.ManyToManyField(salary_element_master, through='RateCardSalaryElement', related_name='rate_cards', blank=True)
    is_active = models.BooleanField(null=True, blank=True, default=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rate_card_created_by', blank=True, null=True, db_column='created_by')
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rate_card_updated_by', blank=True, null=True, db_column='updated_by')
    
    class Meta:
        db_table = 'rate_card_master'
    
    def __str__(self):
        return f"{self.card_name}" if self.card_name else "Unnamed Card"
class RateCardSalaryElement(models.Model):
    rate_card = models.ForeignKey('rate_card_master', on_delete=models.CASCADE)
    salary_element = models.ForeignKey('salary_element_master', on_delete=models.CASCADE)
    
    # Additional fields
    item_name = models.TextField(null=True, blank=True)
    pay_type = models.TextField(null=True, blank=True)
    classification = models.TextField(null=True, blank=True)
    four_hour_amount = models.BigIntegerField(null=True, blank=False)
    nine_hour_amount = models.BigIntegerField(null=True, blank=False)

    class Meta:
        db_table = 'rate_card_salary_element'    
class designation_master(models.Model)    :
    designation_id = models.AutoField(primary_key=True)
    designation_name = models.TextField(null=True,blank=True)
    is_active =models.BooleanField(null=True,blank=True,default=True)
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='designation_master_created_by',blank=True, null=True,db_column='created_by')
    updated_at = models.DateTimeField(null=True,blank=True,auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='designation_master_updated_by',blank=True, null=True,db_column='updated_by')
    class Meta:
        db_table = 'designation_master'
    def __str__(self):
        return f"{self.designation_name}"    
class site_card_relation(models.Model):
    relation_id = models.AutoField(primary_key=True)
    site_id = models.ForeignKey('Masters.site_master', on_delete=models.CASCADE,related_name='site_master_id',blank=True, null=True,db_column='site_id')
    designation_id = models.ForeignKey(designation_master, on_delete=models.CASCADE,related_name='site_designation_master',blank=True, null=True,db_column='designation_id')
    relation_name = models.TextField(null=True,blank=True)
    # working_hours =models.BigIntegerField(null=True,blank=False)
    card_id = models.ForeignKey(rate_card_master, on_delete=models.CASCADE,related_name='rate_card_master_id',blank=True, null=True,db_column='card_id')
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='site_role_card_created_by',blank=True, null=True,db_column='created_by')
    updated_at = models.DateTimeField(null=True,blank=True,auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='site_role_card_updated_by',blank=True, null=True,db_column='updated_by')
    class Meta:
        db_table = 'site_card_relation'
class employee_rate_card_details(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.TextField(null=True,blank=True)
    item_id = models.ForeignKey(salary_element_master, on_delete=models.CASCADE,related_name='employee_rate_card_item_id',blank=True, null=True,db_column='item_id')
    card_id = models.ForeignKey(rate_card_master, on_delete=models.CASCADE,related_name='employee_card_id',blank=True, null=True,db_column='card_id')
    item_name = models.TextField(null=True,blank=True)
    pay_type = models.TextField(null=True,blank=True)
    classification = models.TextField(null=True,blank=True)
    four_hour_amount = models.BigIntegerField(null=True,blank=False)
    nine_hour_amount = models.BigIntegerField(null=True,blank=False)
    is_active =models.BooleanField(null=True,blank=True,default=True)
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='employee_rate_card_created_by',blank=True, null=True,db_column='created_by')
    updated_at = models.DateTimeField(null=True,blank=True,auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='employee_rate_card_updated_by',blank=True, null=True,db_column='updated_by')
    class Meta:
        db_table = 'employee_rate_card_details'  


class slot_attendance_details(models.Model):
    id = models.AutoField(primary_key=True)
    company_id = models.ForeignKey('Masters.company_master', on_delete=models.CASCADE,related_name='attendance_company_id',blank=True, null=True,db_column='company_id')
    site_id = models.ForeignKey('Masters.site_master', on_delete=models.CASCADE,related_name='attendance_site_id',blank=True, null=True,db_column='site_id')
    slot_id = models.ForeignKey('Masters.SlotDetails', on_delete=models.CASCADE,related_name='attendance_slot_id',blank=True, null=True,db_column='slot_id')
    attendance_date = models.DateTimeField(null=True,blank=True)
    attendance_in = models.TextField(null=True,blank=True)
    attendance_out = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='slot_attendance_created_by',blank=True, null=True,db_column='created_by')
    updated_at = models.DateTimeField(null=True,blank=True,auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='slot_attendance_updated_by',blank=True, null=True,db_column='updated_by')
    class Meta:
        db_table = 'slot_attendance_details'  

    
     
    
