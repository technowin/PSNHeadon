# views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from Masters.models import SlotDetails, UserSlotDetails, company_master, sc_employee_master, site_master
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.db.models import Sum
import pandas as pd
from django.views.generic import ListView
from datetime import datetime
from django.db.models import Case, When
# Index (list all salary elements)
@login_required
def index(request):
    salary_elements = salary_element_master.objects.all()
    return render(request, 'Payroll/SalaryElement/index.html', {'salary_elements': salary_elements})

# Create a new salary element
@login_required
def create(request):
    if request.method == 'POST':
        form = SalaryElementMasterForm(request.POST)
        if form.is_valid():
            salary_element = form.save(commit=False)  # Don't save to the database yet
            salary_element.created_by = request.user  # Set created_by to the current user
            salary_element.updated_by = request.user  # Also set updated_by initially
            salary_element.save()  # Now save to the database
            messages.success(request, "Salary Element created successfully!")
            return redirect('salary_element_index')
        else:
            messages.error(request, "Error creating Salary Element.")
    else:
        form = SalaryElementMasterForm()
    
    return render(request, 'Payroll/SalaryElement/create.html', {'form': form})

# Edit an existing salary element
@login_required
def edit(request, pk):
    salary_element = get_object_or_404(salary_element_master, pk=pk)
    
    if request.method == 'POST':
        form = SalaryElementMasterForm(request.POST, instance=salary_element)
        if form.is_valid():
            salary_element = form.save(commit=False)  # Don't save to the database yet
            salary_element.updated_by = request.user  # Also set updated_by initially
            salary_element.save()  # Now save to the database
            messages.success(request, "Salary Element updated successfully!")
            return redirect('salary_element_index')
        else:
            messages.error(request, "Error updating Salary Element.")
    else:
        form = SalaryElementMasterForm(instance=salary_element)
    
    return render(request, 'Payroll/SalaryElement/edit.html', {'form': form, 'salary_element': salary_element})

# View salary element details
@login_required
def view(request, pk):
    salary_element = get_object_or_404(salary_element_master, pk=pk)
    return render(request, 'Payroll/SalaryElement/view.html', {'salary_element': salary_element})


 
@login_required
def rate_card_index(request):
    rate_cards = rate_card_master.objects.all()
    return render(request, 'Payroll/RateCard/index.html', {'rate_cards': rate_cards})

@login_required
def rate_card_create(request):
    if request.method == "POST":
        form = RateCardMasterForm(request.POST)
        if form.is_valid():
            # Save the rate card instance first
            rate_card = form.save(commit=False)
            rate_card.created_by = request.user
            rate_card.updated_by = request.user
            rate_card.is_active = True
            rate_card.save()
            
            # Save the many-to-many relation with additional fields in the through model
            selected_items = request.POST.getlist('item_ids')  # Get selected item_ids
            
            for item_id in selected_items:
                item = salary_element_master.objects.get(pk=item_id)
                four_hour_amount = request.POST.get(f'four_hour_amount_{item_id}', 0)
                nine_hour_amount = request.POST.get(f'nine_hour_amount_{item_id}', 0)
                
                RateCardSalaryElement.objects.create(
                    rate_card=rate_card,
                    salary_element=item,
                    item_name=item.item_name,
                    pay_type=item.pay_type,
                    classification=item.classification,
                    four_hour_amount=four_hour_amount,
                    nine_hour_amount=nine_hour_amount
                )

            messages.success(request, 'Rate Card created successfully!')
            return redirect('rate_card_index')
        else:
            messages.error(request, 'Error creating Rate Card.')
    else:
        form = RateCardMasterForm()
    
    return render(request, 'Payroll/RateCard/create.html', {'form': form})

# @login_required
# def rate_card_edit(request, pk):
#     rate_card = get_object_or_404(rate_card_master, pk=pk)
#     if request.method == "POST":
#         form = RateCardMasterForm(request.POST, instance=rate_card)
#         if form.is_valid():
#             rate_card = form.save(commit=False)
#             item_id = form.cleaned_data['item_id']
#             selected_item = get_object_or_404(salary_element_master, pk=item_id.pk)

#             # Populate the other fields from the selected item
#             rate_card.item_name = selected_item.item_name
#             rate_card.pay_type = selected_item.pay_type
#             rate_card.classification = selected_item.classification
#             rate_card.updated_by = request.user
#             rate_card.save()
#             messages.success(request, 'Rate Card updated successfully!')
#             return redirect('rate_card_index')
#         else:
#             messages.error(request, 'Error updating Rate Card.')
#     else:
#         form = RateCardMasterForm(instance=rate_card)
#     return render(request, 'Payroll/RateCard/edit.html', {'form': form, 'rate_card': rate_card})
# @login_required
# def rate_card_view(request, pk):
#     rate_card = get_object_or_404(rate_card_master, pk=pk)
#     return render(request, 'Payroll/RateCard/view.html', {'rate_card': rate_card})

 
@login_required
def rate_card_edit(request, card_id):
    rate_card = get_object_or_404(rate_card_master, pk=card_id)

    if request.method == "POST":
        form = RateCardMasterForm(request.POST, instance=rate_card)
        if form.is_valid():
            rate_card = form.save(commit=False)
            rate_card.updated_by = request.user
            rate_card.save()

            RateCardSalaryElement.objects.filter(rate_card=rate_card).delete()

            selected_items = request.POST.getlist('item_ids')

            for item_id in selected_items:
                item = salary_element_master.objects.get(pk=item_id)
                four_hour_amount = request.POST.get(f'four_hour_amount_{item_id}', 0)
                nine_hour_amount = request.POST.get(f'nine_hour_amount_{item_id}', 0)

                RateCardSalaryElement.objects.create(
                    rate_card=rate_card,
                    salary_element=item,
                    item_name=item.item_name,
                    pay_type=item.pay_type,
                    classification=item.classification,
                    four_hour_amount=four_hour_amount,
                    nine_hour_amount=nine_hour_amount
                )

            messages.success(request, 'Rate Card updated successfully!')
            return redirect('rate_card_index')
        else:
            messages.error(request, 'Error updating Rate Card.')
    else:
        form = RateCardMasterForm(instance=rate_card)

    selected_item_ids = rate_card.item_ids.values_list('item_id', flat=True)

    # Prepare pre-filled data for each item
    existing_relations = RateCardSalaryElement.objects.filter(rate_card=rate_card)

    prefilled_data = {}
    for relation in existing_relations:
        prefilled_data[relation.salary_element_id] = {
            'four_hour_amount': relation.four_hour_amount,
            'nine_hour_amount': relation.nine_hour_amount
        }

    return render(request, 'Payroll/RateCard/edit.html', {
        'form': form,
        'rate_card': rate_card,
        'selected_item_ids': list(selected_item_ids),
        'prefilled_data': prefilled_data,  # Pass the prefilled amounts
    })

 
@login_required
def rate_card_view(request, card_id):
    rate_card = get_object_or_404(rate_card_master, pk=card_id)
    salary_elements = RateCardSalaryElement.objects.filter(rate_card=rate_card)
    
    return render(request, 'Payroll/RateCard/view.html', {
        'rate_card': rate_card,
        'salary_elements': salary_elements,
    })


@login_required
def site_card_relation_index(request):
    site_card_relations = site_card_relation.objects.all()
    return render(request, 'Payroll/SiteCardRelation/index.html', {'site_card_relations': site_card_relations})
@login_required
def site_card_relation_create(request):
    if request.method == 'POST':
        form = SiteCardRelationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Site Card Relation created successfully!')
            return redirect('site_card_relation_index')
    else:
        form = SiteCardRelationForm()

    return render(request, 'Payroll/SiteCardRelation/create.html', {'form': form})
@login_required
def site_card_relation_edit(request, pk):
    site_card_relation_instance = get_object_or_404(site_card_relation, pk=pk)
    if request.method == 'POST':
        form = SiteCardRelationForm(request.POST, instance=site_card_relation_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Site Card Relation updated successfully!')
            return redirect('site_card_relation_index')
    else:
        form = SiteCardRelationForm(instance=site_card_relation_instance)

    return render(request, 'Payroll/SiteCardRelation/edit.html', {'form': form})
@login_required
def site_card_relation_view(request, pk):
    site_card_relation_instance = get_object_or_404(site_card_relation, pk=pk)
    return render(request, 'Payroll/SiteCardRelation/view.html', {'site_card_relation': site_card_relation_instance})
 
@login_required
def employee_rate_card_index(request):
    rate_cards = employee_rate_card_details.objects.all()
    return render(request, 'Payroll/EmployeeRateCardDetails/index.html', {'rate_cards': rate_cards})
 
@login_required
def employee_rate_card_create(request):
    try:
        # Fetch distinct site_ids and their names
        sites = site_card_relation.objects.all().values('site_id', 'site_id__site_name').distinct()
        
        # Fetch employees not in any rate card
        employees_not_in_rate_card = sc_employee_master.objects.exclude(employee_id__in=employee_rate_card_details.objects.values('employee_id'))

        if request.method == 'POST':
            selected_site_id = request.POST.get('site_id')
            selected_card_id = request.POST.get('card_id')
            selected_employees = request.POST.getlist('selected_employees')  # List of selected employee IDs
            
            # Get the selected rate card
            rate_card = rate_card_master.objects.get(card_id=selected_card_id)

            # Get all RateCardSalaryElement entries for the selected rate card
            rate_card_salary_elements = RateCardSalaryElement.objects.filter(rate_card=rate_card)

            # Loop through each selected employee
            for employee_id in selected_employees:
                # Loop through each salary element related to the rate card
                for rate_card_salary_element in rate_card_salary_elements:
                    employee_rate_card_details.objects.create(
                        employee_id=employee_id,                        # Employee ID from the selected list
                        card_id=rate_card,                              # Foreign key to rate_card_master
                        item_id=rate_card_salary_element.salary_element,  # Foreign key to salary_element_master
                        item_name=rate_card_salary_element.item_name,     # Item name from RateCardSalaryElement
                        pay_type=rate_card_salary_element.pay_type,       # Pay type from RateCardSalaryElement
                        classification=rate_card_salary_element.classification,  # Classification from RateCardSalaryElement
                        four_hour_amount=rate_card_salary_element.four_hour_amount,  # Four hour amount from RateCardSalaryElement
                        nine_hour_amount=rate_card_salary_element.nine_hour_amount,    # Nine hour amount from RateCardSalaryElement
                        created_by=request.user,                        # Assuming current user is creating the record
                        updated_by=request.user 
                    )
            return redirect('employee_rate_card_index')

        return render(request, 'Payroll/EmployeeRateCardDetails/create.html', {
            'sites': sites,
            'employees': employees_not_in_rate_card
        })
    except Exception as e:
        print(str(e))
        return redirect('employee_rate_card_index')
@login_required
def get_rate_cards(request, site_id):
    try:
        rate_cards = site_card_relation.objects.filter(site_id=site_id).select_related('card_id').values(
            'card_id', 'card_id__card_name', 'card_id__is_active', 'card_id__created_at'
        )
        
        cards = [
            {
                'card_id': rc['card_id'],
                'card_name': rc['card_id__card_name'],
                'is_active': rc['card_id__is_active'],
                'created_at': rc['card_id__created_at'],
            } for rc in rate_cards
        ]
        return JsonResponse({'cards': cards})
    except Exception as e:
        print(str(e))
        return JsonResponse({'a':"a"})
@login_required
def employee_rate_card_edit(request, id):
    rate_card_detail = get_object_or_404(employee_rate_card_details, id=id)
    sites = site_card_relation.objects.all().values('site_id', 'site_id__site_name').distinct()
    employees = sc_employee_master.objects.all()

    if request.method == 'POST':
        rate_card_detail.employee_id = request.POST.get('employee_id')
        rate_card_detail.card_id_id = request.POST.get('card_id')  # Store card_id as ForeignKey ID
        rate_card_detail.item_id_id = request.POST.get('item_id')  # Store item_id as ForeignKey ID
        rate_card_detail.four_hour_amount = request.POST.get('four_hour_amount')
        rate_card_detail.nine_hour_amount = request.POST.get('nine_hour_amount')
        rate_card_detail.save()

        return redirect('employee_rate_card_index')

    return render(request, 'Payroll/EmployeeRateCardDetails/edit.html', {
        'rate_card_detail': rate_card_detail,
        'sites': sites,
        'employees': employees
    })
@login_required
def employee_rate_card_view(request, id):
    rate_card_detail = get_object_or_404(employee_rate_card_details, id=id)
    return render(request, 'Payroll/EmployeeRateCardDetails/view.html', {
        'rate_card_detail': rate_card_detail
    })



 
@login_required
def attendance_index(request):
    attendance_records = slot_attendance_details.objects.all()
    return render(request, 'Payroll/Attendance/index.html', {'attendance_records': attendance_records})
 
@login_required
def upload_attendance(request):
    if request.method == 'POST':
        excel_form = ExcelUploadForm(request.POST, request.FILES)
        if excel_form.is_valid():
            excel_file = request.FILES['excel_file']
            data = pd.read_excel(excel_file)
            comp = company_master.objects.get(company_id=request.POST['company_id'])
            site = site_master.objects.get(site_id=request.POST['site_id'])
            slot = SlotDetails.objects.get(slot_id=request.POST['slot_id'])
            for index, row in data.iterrows():
                attendance = slot_attendance_details(
                    company_id= comp ,
                    site_id= site,
                    slot_id= slot,
                    attendance_date=row['attendance_date'],
                    employee_id=row['employee_id'],
                    attendance_in=row['attendance_in'],
                    attendance_out=row['attendance_out'],
                )
                attendance.save()
            messages.success(request, 'Attendance records uploaded successfully.')
            return redirect('attendance_index')

    else:
        excel_form = ExcelUploadForm()

    return render(request, 'Payroll/Attendance/create.html', {
        'excel_form': excel_form,
        'companies': company_master.objects.all()
    })
@login_required
def get_sites(request):
    company_id = request.GET.get('company_id')
    sites = site_master.objects.filter(company_id=company_id).values('site_id', 'site_name')
    return JsonResponse(list(sites), safe=False)
@login_required
def get_slots(request):
    site_id = request.GET.get('site_id')
    slots = SlotDetails.objects.filter(site_id=site_id).values('slot_id', 'slot_name')
    return JsonResponse(list(slots), safe=False)



 
@login_required
def calculate_daily_salary(request,slot_id):
    # Step 1: Fetch employees for the given slot_id from slot_employee_details

    # Step 2: Get the slot details
    slot = SlotDetails.objects.get(slot_id=slot_id)
    employees = slot_employee_details.objects.filter(slot_id=slot_id)
    print(employees)
    generated_logs = salary_generated_log.objects.filter(
    slot_id=slot_id,
    slot_date=slot.shift_date
    ).values_list('employee_id', 'company_id')  # Get both employee_id and company_id as tuples
    print(generated_logs)
    # Exclude employees where the combination of employee_id and company_id is in the generated_logs
    filtered_employees = employees.exclude(
        Q(employee_id__in=[log[0] for log in generated_logs]) & 
        Q(company_id__in=[log[1] for log in generated_logs])
    )
    print(filtered_employees)
    for employee in filtered_employees:
        employee_id = employee.employee_id
        
        # Step 3: Check attendance for the employee in the given slot
        attendance = slot_attendance_details.objects.filter(
            site_id=slot.site_id,
            slot_id=slot_id,
            employee_id=employee_id,
            attendance_date = slot.shift_date
        ).first()
        
        if attendance:
            # Step 4: Calculate the total working hours
            if attendance.attendance_in and attendance.attendance_out:
                if ':' in attendance.attendance_in and ':' in attendance.attendance_out:
                    try:
                       
                        
                        # Convert time_in and time_out to time objects using strptime
                        time_in = datetime.strptime(attendance.attendance_in, '%H:%M').time()
                        time_out = datetime.strptime(attendance.attendance_out, '%H:%M').time()

                        # Calculate working hours
                        time_in_seconds = time_in.hour * 3600 + time_in.minute * 60
                        time_out_seconds = time_out.hour * 3600 + time_out.minute * 60

                        # Handling case where time_out might be on the next day (crossing midnight)
                        if time_out_seconds < time_in_seconds:
                            time_out_seconds += 24 * 3600  # Add 24 hours in seconds to time_out

                        # Calculate the total working hours
                        working_hours = (time_out_seconds - time_in_seconds) / 3600
                    except ValueError:
                    # Handle cases where time conversion fails due to an invalid format
                        working_hours = 0
                        # Step 5: Fetch the rate card from site_card_relation based on site and designation
                    if working_hours !=0:
                        site_card_relation_obj = site_card_relation.objects.filter(
                            site_id=slot.site_id,
                            designation_id=slot.designation_id
                        ).first()

                        if site_card_relation_obj:
                            # Get the rate card ID and related salary elements
                            card_id = site_card_relation_obj.card_id
                            salary_elements = RateCardSalaryElement.objects.filter(rate_card=card_id).annotate(
                            pay_type_order=Case(
                                When(pay_type='Earning', then=1),
                                When(pay_type='Deduction', then=2),
                                When(pay_type='Total', then=3),
                                default=4,  # For any other pay types that are not specified
                                output_field=models.IntegerField(),
                                )
                            ).order_by('pay_type_order', 'item_name')

                            # Step 6: Fetch the BASIC element before looping
                            basic_element = salary_elements.filter(item_name='BASIC').first()
                            basic_amount = 0

                            # Determine BASIC amount based on working hours
                            if basic_element:
                                if working_hours < 9:
                                    basic_amount = basic_element.four_hour_amount
                                else:
                                    basic_amount = basic_element.nine_hour_amount
                            daily_salary.objects.filter(slot_id=slot,
                                employee_id = employee_id,
                                company_id = employee.company_id,
                                attendance_date=attendance.attendance_date).delete()
                            # Step 7: Process each salary element
                            for element in salary_elements:
                                # Step 8: Handle Percentage-based calculations
                                if element.classification == 'Percentage':
                                    if element.item_name == 'DA':
                                        # Calculate percentage based on BASIC
                                        if working_hours < 9:
                                            amount = (basic_amount * element.four_hour_amount) / 100
                                        else:
                                            amount = (basic_amount * element.nine_hour_amount) / 100
                                    else:
                                        # For other percentage-based items, use the normal logic
                                        if working_hours < 9:
                                            amount = (basic_amount * element.four_hour_amount) / 100
                                        else:
                                            amount = (basic_amount * element.four_hour_amount) / 100
                                
                                elif element.classification == "Calculation":
                                    if element.item_name == 'PF':
                                        # Calculate percentage based on BASIC
                                        if working_hours < 9:
                                            amount = (basic_amount * element.four_hour_amount) / 100
                                        else:
                                            amount = (basic_amount * element.nine_hour_amount) / 100
                                    elif element.item_name == 'LWF':
                                        # Calculate percentage based on BASIC
                                        if working_hours < 9:
                                            amount = (basic_amount * element.four_hour_amount) / 100
                                        else:
                                            amount = (basic_amount * element.nine_hour_amount) / 100
                                    elif element.item_name == 'ESIC':
                                        # Calculate percentage based on BASIC
                                        if working_hours < 9:
                                            amount = (basic_amount * element.four_hour_amount) / 100
                                        else:
                                            amount = (basic_amount * element.nine_hour_amount) / 100
                                    elif element.item_name == 'Income Tax':
                                        try:
                                            deduction = income_tax_deduction.objects.get(
                                                employee_id=employee_id,
                                                company_id=employee.company_id.company_id,
                                                deduction_month=attendance.attendance_date.month,
                                                deduction_year = attendance.attendance_date.year,
                                                is_deducted = 0
                                            )
                                            amount = deduction.deduction_amount
                                        except income_tax_deduction.DoesNotExist:
                                            amount = 0
                                    else:
                                        if working_hours < 9:
                                            amount = element.four_hour_amount
                                        else:
                                            amount = element.nine_hour_amount
                                elif element.classification == 'Total' and element.item_name == 'Gross Earning':
                                    # Sum all amounts from daily_salary for this employee, slot, date, and 'earning' pay_type
                                    total_earnings = daily_salary.objects.filter(
                                        employee_id=employee_id,
                                        slot_id=slot_id,
                                        attendance_date=attendance.attendance_date,
                                        pay_type='earning'
                                    ).aggregate(Sum('amount'))['amount__sum'] or 0

                                    amount = total_earnings 
                                elif element.classification == 'Total' and element.item_name == 'Gross Deduction':
                                    # Sum all amounts from daily_salary for this employee, slot, date, and 'earning' pay_type
                                    total_deduction = daily_salary.objects.filter(
                                        employee_id=employee_id,
                                        slot_id=slot_id,
                                        attendance_date=attendance.attendance_date,
                                        pay_type='deduction'
                                    ).aggregate(Sum('amount'))['amount__sum'] or 0
                                    amount = total_deduction
                                elif element.classification == 'Total' and element.item_name == 'Net Salary':
                                    total_earnings = daily_salary.objects.filter(
                                        employee_id=employee_id,
                                        slot_id=slot_id,
                                        attendance_date=attendance.attendance_date,
                                        pay_type='earning'
                                    ).aggregate(Sum('amount'))['amount__sum'] or 0

                                    amount = total_earnings 
                                    # Sum all amounts from daily_salary for this employee, slot, date, and 'earning' pay_type
                                    total_deduction = daily_salary.objects.filter(
                                        employee_id=employee_id,
                                        slot_id=slot_id,
                                        attendance_date=attendance.attendance_date,
                                        pay_type='deduction'
                                    ).aggregate(Sum('amount'))['amount__sum'] or 0
                                    amount = total_earnings - total_deduction           
                                else:
                                    if working_hours < 9:
                                        amount = element.four_hour_amount
                                    else:
                                        amount = element.nine_hour_amount
                                    
                                # Step 9: Insert the record into daily_salary
                                
                                
                                daily_salary.objects.create(
                                    slot_id=slot,
                                    employee_id=employee_id,
                                    company_id = employee.company_id,
                                    attendance_date=attendance.attendance_date,
                                    work_hours=working_hours,
                                    amount=amount,
                                    element_name=element.item_name,
                                    pay_type=element.pay_type,
                                    classification=element.classification,
                                    created_by=request.user,
                                    updated_by=request.user
                                )
                            
                            salary_generated_log.objects.create(slot_id=slot,
                                    employee_id=employee_id,
                                    company_id = employee.company_id,
                                    slot_date=attendance.attendance_date,
                                    created_by=request.user,
                                    updated_by=request.user
                                    )
                            try:
                                deduction = income_tax_deduction.objects.get(
                                    employee_id=employee_id,
                                    company_id=employee.company_id,
                                    deduction_month=attendance.attendance_date.month,
                                    deduction_year=attendance.attendance_date.year,
                                    is_deducted=False
                                )
                                if deduction:
                                    deduction.is_deducted = 1
                                    deduction.deducted_on = attendance.attendance_date
                                    deduction.save()   
                                # Do something with deduction
                            except income_tax_deduction.DoesNotExist:
                                deduction = None  # Handle the case where no deduction is found
                else:
                    # Invalid time format (missing ':')
                    working_hours = 0
            else:
                # Either time_in or time_out is None
                working_hours = 0
    return redirect('slot_list')
class SlotListView(ListView):
    model = SlotDetails
    template_name = 'Payroll/Slot/index.html'
    context_object_name = 'slots'
    paginate_by = 10  # for pagination, optional
def generate_salary_redirect(request, slot_id):
    return redirect('generate_salary', slot_id=slot_id)

@login_required
def user_slot_details_list(request, slot_id):
    slot = get_object_or_404(SlotDetails, slot_id=slot_id)
    user_slot_details = UserSlotDetails.objects.filter(slot_id=slot_id)

    context = {
        'slot': slot,
        'user_slot_details': user_slot_details,
    }
    return render(request, 'Payroll/Slot/user_slot_details.html', context)







 