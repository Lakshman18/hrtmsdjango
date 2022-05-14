from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import DesignationSerializer
from rest_framework.response import Response
from .models import Designation
from Employee.views import checkEmpRole
from rest_framework import status

# Create your views here.

class designation(APIView):
    def get(self,request):
        try:
            # token = checkEmpRole(request.data['token'])
            token = checkEmpRole(request.GET["token"])
            
            if(token['userRole_name'] == 'admin' ):
                try:
                    designation = Designation.objects.all()
                    designation_data = DesignationSerializer(designation, many=True)
                    message = designation_data.data
                    status_code =status.HTTP_200_OK
                except Exception as e:
                    print(e)
                    message="An error Occured. Please try again"
                    status_code =status.HTTP_400_BAD_REQUEST
            else:
                message= "Access denied!"    
                status_code =status.HTTP_400_BAD_REQUEST
        except Exception as e:
            print(e)
            message= "Access denied! Key Missing"
            status_code =status.HTTP_400_BAD_REQUEST  

        return Response({"message":message, "status_code":status_code })

    def post(self, request):
        try:
            token = checkEmpRole(request.data['token'])
            
            if(token['userRole_name'] == 'admin' ):
                designation = Designation.objects.filter(designationName=request.data['designationName']).first()
                if(designation):
                    message ="Designation already exists"
                    status_code =status.HTTP_400_BAD_REQUEST
                else:  
                    try:                          
                        designationSerializer = DesignationSerializer(data = request.data , partial=True)
                        designationSerializer.is_valid(raise_exception=True)
                        designationSerializer.save()
                        message ="Designation created successfully" 
                        status_code =status.HTTP_200_OK               
                    except Exception as e:
                        print(e)
                        message ="An Error Occured. Please check the input values"
                        status_code =status.HTTP_400_BAD_REQUEST
            else:
                message= "Access denied!"    
                status_code =status.HTTP_400_BAD_REQUEST
        except Exception as e:
            print(e)
            message= "Access denied! Key Missing"  
            status_code =status.HTTP_400_BAD_REQUEST
        return Response({"message":message, "status_code":status_code })


    def put (self, request):
        try:
            token = checkEmpRole(request.data['token'])
            
            if(token['userRole_name'] == 'admin' ):            
                designation = Designation.objects.filter(id=request.data['id']).first()
                if(designation):
                    try:
                        designationSerializer = DesignationSerializer(designation, data = request.data, partial=True)
                        if designationSerializer.is_valid():
                            message="Edit successful"
                            status_code =status.HTTP_200_OK
                            designationSerializer.save() 
                        else:
                            message="No matching designation found"
                            status_code =status.HTTP_400_BAD_REQUEST 
                    except Exception as e:
                        print(e)
                        message ="An Error Occured. Please check the input values"  
                        status_code =status.HTTP_400_BAD_REQUEST       
                else:
                    message="No matching designation found"   
                    status_code =status.HTTP_400_BAD_REQUEST
            else:
                message= "Access denied!"  
                status_code =status.HTTP_400_BAD_REQUEST 
        except Exception as e:
            print(e)
            message= "Access denied! Key Missing"
            status_code =status.HTTP_400_BAD_REQUEST
        return Response({"message":message, "status_code":status_code })
