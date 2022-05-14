from rest_framework import serializers
from .models import Vacancy,Applications
from Department.models import Department
from Designation.models import Designation

class VacancySerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.departmentName', required=False)
    designation_name = serializers.CharField(source='designation.designationName', required=False)

    class Meta:
        model = Vacancy
        fields = ['id', 'department', 'department_name', 'designation', 'designation_name', 'no_of_vacancy', 'closingDate',  'createdBy', 'createdDate', 'modifiedBy', 'modifiedDate']


class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Applications
        fields = ['id', 'vacancy', 'applicant_name', 'applicant_email', 'applicant_phone', 'applicant_status', 'applicant_cv',  'modifiedBy', 'modifiedDate']

