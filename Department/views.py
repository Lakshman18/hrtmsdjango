from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import DepartmentSerializer
from rest_framework.response import Response
from .models import Department
from Employee.views import checkEmpRole
from rest_framework import status

# Create your views here.

class departments(APIView):
    def get(self,request):
        try:
            # token = checkEmpRole(request.data['token'])
            token = checkEmpRole(request.GET["token"])
            
            if(token['userRole_name'] == 'admin' ):
                departments = Department.objects.all().values('id','departmentName', 'isActive', 'createdBy', 'createdDate', 'modifiedBy', 'modifiedDate')
                message = departments
                status_code =status.HTTP_200_OK
            else:
                message= "Access denied!"
                status_code =status.HTTP_400_BAD_REQUEST      
        except Exception as e:
            print(e)
            message="An error Occured. Please try again"   
            status_code =status.HTTP_400_BAD_REQUEST 
        return Response({"message":message, "status_code":status_code })

    def post(self, request):
        try:
            token = checkEmpRole(request.data['token'])
            
            if(token['userRole_name'] == 'admin' ):
                department = Department.objects.filter(departmentName=request.data['departmentName']).first()
                if(department):
                    message ="Department already exists"
                    status_code =status.HTTP_400_BAD_REQUEST 
                else:                            
                    departmentSerializer = DepartmentSerializer(data = request.data , partial=True)
                    departmentSerializer.is_valid(raise_exception=True)
                    departmentSerializer.save()
                    message ="Department created successfully" 
                    status_code =status.HTTP_200_OK 
            else:
                message= "Access denied!"
                status_code =status.HTTP_400_BAD_REQUEST                           
        except Exception as e:
            print(e)
            message ="An Error Occured. Please check the input values"
            status_code =status.HTTP_400_BAD_REQUEST 
        return Response({"message":message, "status_code":status_code })


    def put (self, request):
        try:
            token = checkEmpRole(request.data['token'])
            
            if(token['userRole_name'] == 'admin' ):
                department = Department.objects.filter(id=request.data['id']).first()
                if(department):
                    departmentSerializer = DepartmentSerializer(department, data = request.data, partial=True)
                    if departmentSerializer.is_valid():
                        message="Edit successful"
                        status_code =status.HTTP_200_OK
                        departmentSerializer.save() 
                    else:
                        message="No matching department found" 
                        status_code =status.HTTP_400_BAD_REQUEST 
                else:
                    message="No matching department found"   
                    status_code =status.HTTP_400_BAD_REQUEST
            else:
                message= "Access denied!"
                status_code =status.HTTP_400_BAD_REQUEST   
        except Exception as e:
            print(e)
            message ="An Error Occured. Please check the input values"
            status_code =status.HTTP_400_BAD_REQUEST
        return Response({"message":message, "status_code":status_code })
