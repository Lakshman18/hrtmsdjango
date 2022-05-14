from rest_framework import serializers
from .models import Designation

class DesignationSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.departmentName', required=False)
    
    class Meta:
        model = Designation
        fields = ['id', 'designationName', 'department', 'department_name', 'description','isActive', 'createdBy', 'createdDate', 'modifiedBy', 'modifiedDate']
