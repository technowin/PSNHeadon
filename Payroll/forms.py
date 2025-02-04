# forms.py
from django import forms

from Account.models import user_role_map
from Masters.models import parameter_master, site_master
from .models import *

class SalaryElementMasterForm(forms.ModelForm):
    class Meta:
        model = salary_element_master
        fields = ['item_name', 'pay_type', 'classification','tax_parameter']
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'pay_type': forms.Select(attrs={'class': 'form-control'}),
            'classification': forms.Select(attrs={'class': 'form-control'}),
            'tax_parameter': forms.Select(attrs={'class': 'form-control'}),
        }


class RateCardMasterForm(forms.ModelForm):
    item_ids = forms.ModelMultipleChoiceField(
        queryset=salary_element_master.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Customize widget if necessary
        required=False
    )
    
    class Meta:
        model = rate_card_master
        fields = ['card_name', 'item_ids']
        widgets = {
            'card_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter card name'}),  # Override Textarea to TextInput
        }

class SiteCardRelationForm(forms.ModelForm):
    class Meta:
        model = site_card_relation
        fields = ['site', 'relation_name', 'card', 'designation']
        widgets = {
            'relation_name': forms.TextInput(attrs={'class': 'form-control'}),
            'site': forms.Select(attrs={'class': 'form-control'}),
            'card': forms.Select(attrs={'class': 'form-control'}),
            'designation': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)  # Extract user_id from kwargs
        super(SiteCardRelationForm, self).__init__(*args, **kwargs)

        if user_id is not None:
            # Filter the site field based on user_role_map
            self.fields['site'].queryset = site_master.objects.filter(
                site_id__in=user_role_map.objects.filter(user_id=user_id).values_list('site_id', flat=True)
            )


        
class SlotAttendanceForm(forms.ModelForm):
    class Meta:
        model = slot_attendance_details
        fields = ['company_id', 'site_id', 'slot_id', 'attendance_date', 'attendance_in', 'attendance_out']

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()        
        