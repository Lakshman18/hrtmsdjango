from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    employee_First_name = serializers.CharField(source='employee.firstName', required=False)
    employee_Last_name = serializers.CharField(source='employee.lastName', required=False)

    class Meta:
        model = Attendance
        fields = ['id','employee', 'employee_First_name', 'employee_Last_name', 'date', 'inTime', 'outTime']