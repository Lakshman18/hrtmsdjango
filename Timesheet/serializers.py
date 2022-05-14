from rest_framework import serializers
from .models import Timesheet


class TimesheetSerializer(serializers.ModelSerializer):
    employee_First_name = serializers.CharField(source='employee.firstName', required=False)
    employee_Last_name = serializers.CharField(source='employee.lastName', required=False)
    project_name = serializers.CharField(source='project.projectName', required=False)

    class Meta:
        model = Timesheet
        fields = ['id', 'employee','employee_First_name', 'employee_Last_name', 'project', 'project_name', 'date', 'startTime', 'endTime', 'activity']
