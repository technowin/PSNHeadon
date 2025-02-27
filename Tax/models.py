from django.db import models

from Account.models import CustomUser


class Slab(models.Model):
    id = models.AutoField(primary_key=True)
    slab_id = models.ForeignKey('Tax.SlabMaster', on_delete=models.CASCADE,blank=True, null=True,db_column ='slab_id')
    salary_from =  models.FloatField(null=True,blank=True)
    salary_to =  models.FloatField(null=True,blank=True)
    salary_deduct =  models.FloatField(null=True,blank=True)
    slab_status =  models.FloatField(null=True,blank=True)
    slab_type =  models.CharField(max_length=253,null=True,blank=True)
    slab_for =  models.CharField(max_length=255,null=True,blank=True)
    effective_date = models.DateField(null=True,blank=True)
    applicable_designation =  models.CharField(max_length=255,null=True,blank=True)   
    lwf_applicable =  models.FloatField(null=True,blank=True)
    employee_min_amount =  models.IntegerField(null=True,blank=True)
    special_LWF_calculation =  models.FloatField(null=True,blank=True)
    special_employer_contribution =  models.IntegerField(null=True,blank=True)
    employer_min_amount =  models.IntegerField(null=True,blank=True)
    Lwf_Type =  models.CharField(max_length=255,null=True,blank=True)
    slab_applicable = models.CharField(max_length=255, null=True, blank=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True, related_name='slabb_created_by',db_column='created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True, related_name='slabb_updated_by' ,db_column ='updated_by')

    class Meta:
        db_table = 'tbl_slab'


class SlabMaster(models.Model):
    slab_id = models.AutoField(primary_key=True)
    act_id = models.ForeignKey('Tax.ActMaster', on_delete=models.CASCADE,blank=True, null=True,db_column='act_id')
    state = models.ForeignKey('Masters.StateMaster', on_delete=models.CASCADE,related_name='slab_tax_state',blank=True, null=True, db_column='state_id')
    act_by = models.CharField(max_length=255,null=True, blank=True)
    city = models.ForeignKey('Masters.CityMaster', on_delete=models.CASCADE,related_name='slab_tax_city',blank=True, null=True, db_column='city_id')
    is_slab =models.CharField(max_length=255)
    slab_freq =models.CharField(max_length=255)
    slab_status =models.FloatField(null=True,blank=True)
    slab_year =models.CharField(max_length=255)
    slab_months =models.CharField(max_length=255)
    slab_months_challan =models.CharField(max_length=255,null=True,blank=True)
    period =models.CharField(max_length=255,null=True,blank=True)
    exception_month = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True, related_name='slab_created_by',db_column='created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True, related_name='slab_updated_by',db_column ='updated_by') 
  
    class Meta:
        db_table = 'tbl_slab_master'


class TaxCalculation(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.CharField(max_length=100, null=True, blank=True)
    company = models.ForeignKey('Masters.company_master', blank=True, null=True,on_delete=models.CASCADE, related_name='tax_company')
    site = models.ForeignKey('Masters.site_master', on_delete=models.CASCADE,related_name='tax_site',blank=True, null=True, db_column='site_id')
    state = models.ForeignKey('Masters.StateMaster', on_delete=models.CASCADE,related_name='tax_state',blank=True, null=True, db_column='state_id')
    city = models.IntegerField(null=True,blank=True)
    act = models.ForeignKey('Tax.ActMaster', on_delete=models.CASCADE,related_name='tax_act',blank=True, null=True, db_column='act_id')
    month = models.CharField(max_length=50, null=True, blank=True)
    year = models.CharField(max_length=50, null=True, blank=True)
    slab_freq = models.CharField(max_length=50, null=True, blank=True)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    employee_tax = models.FloatField(null=True, blank=True)
    tax_deducted = models.IntegerField(null=True,blank=True)
    remarks = models.CharField(max_length=500, null=True, blank=True)
    challan_month = models.CharField(max_length=50, null=True, blank=True)
    challan_year = models.CharField(max_length=50, null=True, blank=True)
    challan_period = models.CharField(max_length=500, null=True, blank=True)
    employer_deduct = models.FloatField(null=True, blank=True)
    status = models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True, related_name='tax_created_by',db_column='created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True, related_name='tax_updated_by',db_column ='updated_by')
                         
    class Meta:
        db_table = 'tax_calculation' 


class ActMaster(models.Model):
    act_id = models.AutoField(primary_key=True)
    act_name =   models.CharField(max_length=265,null=True,blank=True)
    act_menu_name =  models.CharField(max_length=265,null=True,blank=True)
    act_status = models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True, related_name='act_created_by', db_column='created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True, related_name='act_updated_by',db_column ='updated_by')
    class Meta:
        db_table = 'tbl_act_master'
    def __str__(self):
        return self.act_name
    

class FinancialYear(models.Model):
    id = models.AutoField(primary_key=True)
    year =  models.CharField(max_length=255,null=True,blank=True)
    class Meta:
        db_table = 'financial_year'
    def __str__(self):
        return self.year
