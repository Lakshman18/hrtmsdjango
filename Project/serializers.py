from dataclasses import field
from rest_framework import serializers
from .models import Project
from Employee.models import Employee
from Employee.serializers import EmployeeSerializer

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id','firstName', 'lastName', 'isActive' )


class ProjectSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', required=False)

    class Meta:
        model = Project
        fields = ['id', 'projectName', 'client', 'client_name', 'employee', 'startDate', 'renewalDate', 'createdBy', 'createdDate', 'modifiedBy', 'modifiedDate', 'isActive']


class ProjectViewSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', required=False)
    employee = EmployeeSerializer(many=True, read_only=True , required=False)

    class Meta:
        model = Project
        fields = ['id', 'projectName', 'client', 'client_name', 'employee', 'startDate', 'renewalDate', 'createdBy', 'createdDate', 'modifiedBy', 'modifiedDate', 'isActive']
