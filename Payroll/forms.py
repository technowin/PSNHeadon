# forms.py
from django import forms
from .models import *

class SalaryElementMasterForm(forms.ModelForm):
    class Meta:
        model = salary_element_master
        fields = ['item_name', 'pay_type', 'classification']
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'pay_type': forms.TextInput(attrs={'class': 'form-control'}),
            'classification': forms.TextInput(attrs={'class': 'form-control'}),
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
        fields = ['site_id', 'relation_name', 'card_id','designation_id']
        widgets = {
            'relation_name': forms.TextInput(attrs={'class': 'form-control'}),
            'site_id': forms.Select(attrs={'class': 'form-control'}),
            'card_id': forms.Select(attrs={'class': 'form-control'}),
            'designation_id': forms.Select(attrs={'class': 'form-control'}),
        }