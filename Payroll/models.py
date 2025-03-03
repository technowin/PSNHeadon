from django.db import models

from Account.models import CustomUser
# from Masters.models import SlotDetails, company_master, site_master

# Create your models here.
class salary_element_master(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.TextField(null=True,blank=True)
    pay_type = models.ForeignKey('Payroll.pay_type', on_delete=models.CASCADE,related_name='salary_pay_relation',blank=True, null=True,db_column='pay_type')
    classification = models.ForeignKey('Payroll.basis_type', on_delete=models.CASCADE,related_name='salary_basis_relation',blank=True, null=True,db_column='classification')
    is_active = models.BooleanField(null=True,blank=True,default=True)
    tax_parameter = models.ForeignKey('Payroll.income_tax_parameter', on_delete=models.CASCADE,related_name='salary_income_related',blank=True, null=True,db_column='tax_parameter')
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='salary_item_created_by',blank=True, null=True,db_column='created_by')
    updated_at = models.DateTimeField(null=True,blank=True,auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='salary_item_updated_by',blank=True, null=True,db_column='updated_by')
    class Meta:
        db_table = 'salary_element_master'
    def __str__(self):
        return f"{self.item_name} - {self.pay_type} - {self.classification}"
    

class pay_type(models.Model):
    pay_id = models.AutoField(primary_key=True)
    name = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='pay_created_by',blank=True, null=True,db_column='created_by')
    updated_at = models.DateTimeField(null=True,blank=True,auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='pay_updated_by',blank=True, null=True,db_column='updated_by')
    class Meta:
        db_table = 'pay_type'
    def __str__(self):
        return self.name

class basis_type(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='basis_created_by',blank=True, null=True,db_column='created_by')
    updated_at = models.DateTimeField(null=True,blank=True,auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='basis_updated_by',blank=True, null=True,db_column='updated_by')
    class Meta:
        db_table = 'basis_type'
    def __str__(self):
        return self.name
    
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
    tax_parameter = models.ForeignKey('Payroll.income_tax_parameter', on_delete=models.CASCADE,related_name='rate_card_income_related',blank=True, null=True,db_column='tax_parameter')
    four_hour_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    nine_hour_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

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
    site = models.ForeignKey('Masters.site_master', on_delete=models.CASCADE,related_name='site_master_id',blank=True, null=True,db_column='site_id')
    designation = models.ForeignKey(designation_master, on_delete=models.CASCADE,related_name='site_designation_master',blank=True, null=True,db_column='designation_id')
    relation_name = models.TextField(null=True,blank=True)
    # working_hours =models.BigIntegerField(null=True,blank=False)
    card= models.ForeignKey(rate_card_master, on_delete=models.CASCADE,related_name='rate_card_master_id',blank=True, null=True,db_column='card_id')
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='site_role_card_created_by',blank=True, null=True,db_column='created_by')
    updated_at = models.DateTimeField(null=True,blank=True,auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='site_role_card_updated_by',blank=True, null=True,db_column='updated_by')
    class Meta:
        unique_together=['site','card','designation']
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
    site_id = models.ForeignKey('Masters.site_master', on_delete=models.CASCADE,related_name='attendance_site_id1',blank=True, null=True,db_column='site_id')
    slot_id = models.ForeignKey('Masters.SlotDetails', on_delete=models.CASCADE,related_name='attendance_slot_id',blank=True, null=True,db_column='slot_id')
    attendance_date = models.DateField(null=True,blank=True)
    attendance_in = models.TextField(null=True,blank=True)
    employee_id = models.TextField(max_length=250,null=True,blank=True)
    attendance_out = models.TextField(null=True,blank=True)
    status = models.ForeignKey('Payroll.StatusMaster', on_delete=models.CASCADE,related_name='attendance_status',blank=True, null=True,db_column='status_id')
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='slot_attendance_created_by',blank=True, null=True,db_column='created_by')
    updated_at = models.DateTimeField(null=True,blank=True,auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='slot_attendance_updated_by',blank=True, null=True,db_column='updated_by')
    class Meta:
        db_table = 'slot_attendance_details'  

    
class slot_employee_details(models.Model):
    id = models.AutoField(primary_key=True)
    slot_id = models.ForeignKey('Masters.SlotDetails', on_delete=models.CASCADE,related_name='employee_slot_id',blank=True, null=True,db_column='slot_id')
    employee_id = models.TextField(max_length=250,null=True,blank=True)
    company_id = models.ForeignKey('Masters.company_master', on_delete=models.CASCADE,related_name='slot_employee_company_id',blank=True, null=True,db_column='company_id')
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='slot_employee_created_by',blank=True, null=True,db_column='created_by')
    updated_at = models.DateTimeField(null=True,blank=True,auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='slot_employee_updated_by',blank=True, null=True,db_column='updated_by')
    class Meta:
        db_table = 'slot_employee_details'  
    

class daily_salary(models.Model):
    id = models.AutoField(primary_key=True)
    slot_id = models.ForeignKey('Masters.SlotDetails', on_delete=models.CASCADE, related_name='daily_salary_slot_id', db_column='slot_id')
    employee_id = models.TextField(max_length=250, null=True, blank=True)
    company_id = models.ForeignKey('Masters.company_master', on_delete=models.CASCADE, related_name='daily_salary_company_id', db_column='company_id',null=True,blank=True)
    attendance_date = models.DateField(null=True, blank=True)
    work_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Total working hours
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Salary amount for the day
    element_name = models.TextField(null=True, blank=True)  # From salary elements
    pay_type = models.TextField(null=True, blank=True) 
    tax_parameter = models.ForeignKey('Payroll.income_tax_parameter', on_delete=models.CASCADE,related_name='daily_salary_income_related',blank=True, null=True,db_column='tax_parameter') # From salary elements
    classification = models.TextField(null=True, blank=True)  # From salary elements
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='daily_salary_created_by', blank=True, null=True, db_column='created_by')
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='daily_salary_updated_by', blank=True, null=True, db_column='updated_by')

    class Meta:
        db_table = 'daily_salary'

class salary_generated_log(models.Model):
    id = models.AutoField(primary_key=True)
    slot_id = models.ForeignKey('Masters.SlotDetails', on_delete=models.CASCADE, related_name='sal_gen_log_slot_id', db_column='slot_id')
    employee_id = models.TextField(max_length=250, null=True, blank=True)
    company_id = models.ForeignKey('Masters.company_master', on_delete=models.CASCADE, related_name='sal_gen_log_company_id', db_column='company_id')
    slot_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sal_gen_log_created_by', blank=True, null=True, db_column='created_by')
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sal_gen_log_updated_by', blank=True, null=True, db_column='updated_by')
    class Meta:
        db_table = 'salary_generated_log'

class income_tax_deduction(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.TextField(max_length=250, null=True, blank=True)
    company_id = models.ForeignKey('Masters.company_master', on_delete=models.CASCADE, related_name='income_tax_deduction_company_id', db_column='company_id')
    deduction_month = models.IntegerField(null=True, blank=True)
    deduction_year = models.IntegerField(null=True, blank=True)
    deducted_on = models.DateField(null=True,blank=False)
    deduction_amount = models.BigIntegerField(null=True, blank=True)
    is_deducted = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='income_tax_deduction_created_by', blank=True, null=True, db_column='created_by')
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='income_tax_deduction_updated_by', blank=True, null=True, db_column='updated_by')
    class Meta:
        db_table = 'income_tax_deduction'
    
    
    
class StatusMaster(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_type = models.TextField(max_length=100, null=True, blank=True)
    status_name = models.TextField(max_length=100, null=True, blank=True)
    class Meta:
        db_table = 'status_master'
        
        
class PayoutDetails(models.Model):
    payout_id = models.AutoField(primary_key=True)
    # employee_id = models.ForeignKey('Masters.sc_employee_master', on_delete=models.CASCADE, related_name='payout_employee')
    employee_id = models.TextField(null=True, blank=True)
    company_id = models.ForeignKey('Masters.company_master', on_delete=models.CASCADE, related_name='payout_company', db_column='company_id')
    slot_id = models.ForeignKey('Masters.SlotDetails', on_delete=models.CASCADE, related_name='payout_slot')
    site_id = models.ForeignKey('Masters.site_master', on_delete=models.CASCADE,related_name='payout_site',blank=True, null=True, db_column='site_id')
    
    # Razorpay response fields
    razorpay_payout_id = models.CharField(max_length=100, null=True, blank=True) 
    fund_account_id = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fees = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    utr = models.CharField(max_length=100, null=True, blank=True)
    failure_reason = models.TextField(null=True, blank=True)
    payout_status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, related_name='payout_status')

    payout_for_date = models.DateField(null=True, blank=True)
    payment_initiated_date = models.DateTimeField(null=True, blank=True)
    payment_completed_date = models.DateTimeField(null=True, blank=True)
    reference_id = models.TextField(max_length=100, null=True, blank=True)
    purpose = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payout_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payout_updated_by')

    class Meta:
        db_table = 'payout_details'

class payment_details(models.Model):
    id = models.AutoField(primary_key=True)
    account_number = models.CharField(max_length=100, null=True, blank=True) 
    currency = models.TextField(max_length=250,null=True,blank=True)
    mode = models.TextField(max_length=250,null=True,blank=True)
    purpose = models.TextField(max_length=250,null=True,blank=True)
    api_key = models.TextField(max_length=250,null=True,blank=True)
    secret_key = models.TextField(max_length=250,null=True,blank=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,related_name='payment_created_by')
    updated_at = models.DateTimeField(blank=True, null=True,auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True, related_name='payment_updated_by')
    class Meta:
        db_table = 'payment_details'


class BankDetails(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id =models.TextField(null=True,blank=True)
    company = models.ForeignKey('Masters.company_master', blank=True, null=True,on_delete=models.CASCADE, related_name='bank_company')
    bank_name = models.TextField(null=True,blank=True)
    branch_name = models.TextField(null=True,blank=True)
    account_no =  models.TextField(null=True,blank=True)
    account_holder_name =  models.TextField(null=True,blank=True)
    ifsc_code =  models.TextField(null=True,blank=True)
    initiated_date = models.DateTimeField(null=True, blank=True)
    failed_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    utr = models.CharField(max_length=100, null=True, blank=True)
    failure_reason = models.TextField(null=True, blank=True)
    reference_id = models.TextField(null=True,blank=True)
    status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, related_name='bank_status')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True, related_name='bank_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True, related_name='bank_updated_by')

    class Meta:
        db_table = 'bank_details'

class BankDetailAPI(models.Model):
    id = models.AutoField(primary_key=True)
    api_key = models.TextField(null=True,blank=True)
    secret_key = models.TextField(null=True,blank=True)
    url= models.TextField(null=True,blank=True)
    type = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True, related_name='bankAPI_created_by')
    class Meta:
        db_table = 'bank_detailAPi'

class PaySlip(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.CharField(max_length=255)
    slot_id = models.ForeignKey('Masters.SlotDetails', on_delete=models.CASCADE, related_name='pay_slip_slot_id', db_column='slot_id')
    pdf_file = models.FileField(upload_to='payslips/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True, related_name='pay_slip_created_by')
    class Meta:
        db_table = 'pay_slip_data'

class IncomeTaxMaster(models.Model):
    id = models.AutoField(primary_key=True)
    financial_year = models.TextField(null=True,blank=True)
    tax_slab_from = models.TextField(null=True,blank=True)
    tax_slab_to = models.TextField(null=True,blank=True)
    tax_rate = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='income_tax_master_created_by', blank=True, null=True, db_column='created_by')
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='income_tax_master_updated_by', blank=True, null=True, db_column='updated_by')
    class Meta:
        db_table = 'income_tax_master'

class IncomeTaxCalculation(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.TextField(null=True,blank=True)
    total_gross = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    period = models.TextField(null=True,blank=True)
    financial_year = models.TextField(null=True,blank=True)
    total_income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    standard_deduction = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_pt = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    taxable_income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_80c = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    remaining_taxable_income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rebate_under_87a = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    edu_cess = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_tax_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pending_tax_mount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_tax_paid = models.DateField(null=True, blank=True, auto_now_add=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='income_tax_created_by', blank=True, null=True, db_column='created_by')
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='income_tax_updated_by', blank=True, null=True, db_column='updated_by')
    class Meta:
        db_table = 'income_tax_calculation'

class income_tax_parameter(models.Model):
    id = models.AutoField(primary_key=True)
    tax_parameter = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='income_tax_parameter_created_by', blank=True, null=True, db_column='created_by')
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='income_tax_parameter_updated_by', blank=True, null=True, db_column='updated_by')
    class Meta:
        db_table = 'income_tax_parameter'
    def __str__(self):
        return f"{self.tax_parameter}"  













