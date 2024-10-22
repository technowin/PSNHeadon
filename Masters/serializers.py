from rest_framework import serializers

from Masters.models import *

 
class CompanyMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = company_master
        fields = '__all__'  # Include all fields, or specify specific fields as needed


class ParameterMasterSerializer(serializers.ModelSerializer):  # Corrected serializer class name
    class Meta:
        model = parameter_master  # Assuming the model name is in PascalCase, adjust if necessary
        fields = '__all__'  # This will include all fields in the serialization


class ScRosterSerializer(serializers.ModelSerializer):
    company = CompanyMasterSerializer()  # Use the nested serializer

    class Meta:
        model = sc_roster
        fields = '__all__'  

class StateMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateMaster
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    state_id = StateMasterSerializer()
    company_id = CompanyMasterSerializer()
    employement_status_id = ParameterMasterSerializer()
    class Meta:
        model = sc_employee_master
        fields = '__all__' 
