from django import forms

from Account.models import user_role_map
from Masters.models import CityMaster, StateMaster, parameter_master
from .models import *


class StateMasterForm(forms.ModelForm):
    STATE_CHOICES = [
        (True, 'Active'),
        (False, 'Inactive'),
    ]

    state_status = forms.ChoiceField(
        choices=STATE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = StateMaster
        fields = ['state_name','state_status']
        widgets = {
            'state_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CityMasterForm(forms.ModelForm):
    CITY_CHOICES = [
        (True, 'Active'),
        (False, 'Inactive'),
    ]

    city_status = forms.ChoiceField(
        choices=CITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CityMaster
        fields = ['city_name','city_status']
        widgets = {
            'city_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ActMasterForm(forms.ModelForm):
    ACT_CHOICES = [
        (True, 'Active'),   # Display Active for True
        (False, 'Inactive') # Display Inactive for False
    ]

    act_status = forms.ChoiceField(
        choices=ACT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = ActMaster
        fields = ['act_name', 'act_menu_name']
        widgets = {
            'act_name': forms.TextInput(attrs={'class': 'form-control'}),
            'act_menu_name': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',  # Make the field read-only
                'id': 'act_menu_name'   # Add ID for JavaScript
            }),
        }

    def clean_act_status(self):
        """Convert True/False to 1/0 before saving."""
        act_status = self.cleaned_data['act_status']
        return 1 if act_status == 'True' else 0
    
class SlabForm(forms.ModelForm):
    class Meta:

        slab_for = forms.ModelChoiceField(
            queryset=parameter_master.objects.filter(parameter_name='slab_for'),  # Filter for 'slab_for'
            to_field_name='parameter_value',
            empty_label='Select Slab For',
            widget=forms.Select(attrs={'class': 'form-control'})
        )

        slab_applicable = forms.ModelChoiceField(
            queryset=parameter_master.objects.filter(parameter_name='slab_applicable'),  # Filter for 'slab_applicable'
            to_field_name='parameter_value',
            empty_label='Select Slab Applicable',
            widget=forms.Select(attrs={'class': 'form-control'})
        )

        Lwf_Type = forms.ModelChoiceField(
            queryset=parameter_master.objects.filter(parameter_name='LWF Type'),  # Filter for 'lwf_type'
            to_field_name='parameter_value',
            empty_label='Select LWF Type',
            widget=forms.Select(attrs={'class': 'form-control'})
        )

        SLAB_STATUS_CHOICES = [
        (1, 'Active'),
        (0, 'Inactive'),
        ]
        model = Slab
        fields = [
            'salary_from', 'salary_to', 'salary_deduct', 'slab_for', 'effective_date', 
            'applicable_designation', 'lwf_applicable', 'employee_min_amount', 'special_LWF_calculation', 
            'special_employer_contribution', 'employer_min_amount', 'Lwf_Type', 'slab_applicable', 'slab_status'
        ]
        widgets = {
            'salary_from': forms.NumberInput(attrs={'class': 'form-control'}),
            'salary_to': forms.NumberInput(attrs={'class': 'form-control'}),
            'salary_deduct': forms.NumberInput(attrs={'class': 'form-control'}),
            'effective_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'applicable_designation': forms.TextInput(attrs={'class': 'form-control'}),
            'lwf_applicable': forms.NumberInput(attrs={'class': 'form-control'}),
            'employee_min_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'special_LWF_calculation': forms.NumberInput(attrs={'class': 'form-control'}),
            'special_employer_contribution': forms.NumberInput(attrs={'class': 'form-control'}),
            'employer_min_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'slab_status': forms.Select(choices=SLAB_STATUS_CHOICES, attrs={'class': 'form-control'}),
        }

    # Custom fields to handle the dropdowns
   

   
class SlabMasterForm(forms.ModelForm):
    slab_year = forms.ModelChoiceField(
        queryset=FinancialYear.objects.all(),
        empty_label="Select a year",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Slab Year",
        to_field_name='year' 
    )

    slab_freq = forms.ModelChoiceField(
        queryset=parameter_master.objects.filter(parameter_name='Frequency'),
        empty_label="Select Frequency",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Slab Frequency",
        to_field_name='parameter_value'
    )

    period = forms.ModelChoiceField(
        queryset=parameter_master.objects.filter(parameter_name='Period'),
        empty_label="Select Period",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Period",
        to_field_name='parameter_value'
    )

    act_by = forms.ModelChoiceField(
        queryset=parameter_master.objects.filter(parameter_name='act_by'),
        empty_label="Select Act",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Act By",
        to_field_name='parameter_value'
    )

    # Choice field for is_slab
    is_slab = forms.ChoiceField(
        choices=[('Yes', 'Yes'), ('No', 'No')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Is Slab Applicable"
    )


    slab_status = forms.ChoiceField(
        choices=[(1.0, 'Active'), (0.0, 'Inactive')],  # Float values for choices
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Slab Status"
    )


    class Meta:
        model = SlabMaster
        fields = ['slab_year', 'act_id', 'state', 'city', 'is_slab', 'slab_freq','period','act_by','is_slab','slab_status']
        widgets = {
            'act_id': forms.Select(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
        }


   

