from rest_framework import serializers
from .models import Role, Employee

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id','name', 'description', 'isActive', 'createdBy', 'createdDate', 'modifiedBy', 'modifiedDate']

class EmployeeSerializer(serializers.ModelSerializer):
    userRole_name = serializers.CharField(source='userRole.name', required=False)
    department_name = serializers.CharField(source='department.departmentName', required=False)
    designation_name = serializers.CharField(source='designation.designationName', required=False)
    manager_first_name = serializers.CharField(source='manager.firstName', required=False)
    manager_last_name = serializers.CharField(source='manager.lastName', required=False)

    class Meta:
        model = Employee
        fields = ['id', 'firstName', 'lastName' ,'email' , 'password', 'userRole', 'userRole_name', 'nic', 
            'emergencyContact', 'gender',  'department', 'department_name', 'designation', 'designation_name', 
            'manager', 'manager_first_name', 'manager_last_name', 'dateOfJoining', 'phoneNumber' , 'dob', 'religion' ,'maritualStatus' ,'isActive', 
            'availableAnnualLeave', 'availableCasualLeave', 'availableSickLeave', 'address', 'image', 'createdBy', 
            'createdDate', 'modifiedBy', 'modifiedDate']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()    
        return instance
