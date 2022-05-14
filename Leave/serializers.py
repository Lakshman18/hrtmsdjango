from rest_framework import serializers
from .models import Leave

class LeaveSerializer(serializers.ModelSerializer):
    employee_First_name = serializers.CharField(source='employee.firstName', required=False)
    employee_Last_name = serializers.CharField(source='employee.lastName', required=False)
    
    class Meta:
        model = Leave
        fields = ['id','employee_First_name', 'employee_Last_name', 'employee', 'leaveFromDate','leaveToDate', 'reason', 'status', 'createdDate', 'modifiedBy', 'modifiedDate']
