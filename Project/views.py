from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ProjectSerializer, ProjectViewSerializer
from rest_framework.response import Response
from .models import Project as ProjectModel
from Client.models import Client
from Employee.models import Employee
from Employee.views import checkEmpRole
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status

# Create your views here.

class Project(APIView):
    def get(self,request):
        try:
            # token = checkEmpRole(request.data['token'])
            token = checkEmpRole(request.GET["token"])
            
            if(token['userRole_name'] == 'admin' ):
                try:
                    project = ProjectModel.objects.all()
                    project_data = ProjectViewSerializer(project, many=True)
                    message=project_data.data
                    status_code =status.HTTP_200_OK
                except Exception as e:
                    print(e)
                    message="An error Occured. Please try again" 
                    status_code =status.HTTP_400_BAD_REQUEST
                    
            elif(token['userRole_name'] == 'employee' or token['userRole_name'] == 'manager'):
                try:
                    project = ProjectModel.objects.filter(employee = token['id']).filter(isActive=1)
                    project_data = ProjectSerializer(project, many=True)
                    message=project_data.data
                    status_code =status.HTTP_200_OK
                except Exception as e:
                    print(e)
                    message="An error Occured. Please try again"
                    status_code =status.HTTP_400_BAD_REQUEST  
            # elif(token['userRole_name'] == 'client'):
            #     try:
            #         project = ProjectModel.objects.filter(client = )
            #         project_data = ProjectSerializer(project, many=True)
            #         message=project_data.data
            #     except Exception as e:
            #         print(e)
            #         message="An error Occured. Please try again"                        
            else:
                message= "Access denied!"   
                status_code =status.HTTP_400_BAD_REQUEST 
        except:
            message= "Access denied! Key Missing" 
            status_code =status.HTTP_400_BAD_REQUEST         
        return Response({"message":message, "status_code":status_code })


    def post(self, request):
        try:
            token = checkEmpRole(request.data['token'])
            
            if(token['userRole_name'] == 'admin' ):
                try:
                    project = ProjectModel.objects.filter(client=request.data['client'], projectName=request.data['projectName']).first()
                    if(project):
                        message ="project already exists"
                        status_code =status.HTTP_400_BAD_REQUEST
                    else:              
                        projectSerializer = ProjectSerializer(data = request.data , partial=True)
                        projectSerializer.is_valid(raise_exception=True)
                        projectSerializer.save()
                        message ="project created successfully"
                        status_code =status.HTTP_200_OK                
                except Exception as e:
                    print(e)
                    message ="An Error Occured. Please check the input values"
                    status_code =status.HTTP_400_BAD_REQUEST
            else:
                message= "Access denied!"    
                status_code =status.HTTP_400_BAD_REQUEST
        except:
            message= "Access denied! Key Missing"  
            status_code =status.HTTP_400_BAD_REQUEST   
        return Response({"message":message, "status_code":status_code })


    def put (self, request):
        try:
            token = checkEmpRole(request.data['token'])
            print(request.data['id'])
            
            if(token['userRole_name'] == 'admin' ):
                try:
                    project = ProjectModel.objects.filter(id=request.data['id']).first()
                    if(project):
                        projectSerializer = ProjectSerializer(project, data = request.data, partial=True)
                        if projectSerializer.is_valid(raise_exception=True):
                            message="Edit successful"
                            status_code =status.HTTP_200_OK
                            projectSerializer.save() 
                        else:
                            message="An Error Occured"
                            status_code =status.HTTP_400_BAD_REQUEST
                    else:
                        message="No matching project found!"
                        status_code =status.HTTP_400_BAD_REQUEST
                except Exception as e:
                    print(e)
                    message ="An Error Occured. Please check the input values"
                    status_code =status.HTTP_400_BAD_REQUEST
            else:
                message= "Access denied!"  
                status_code =status.HTTP_400_BAD_REQUEST  
        except:
            message= "Access denied! Key Missing"   
            status_code =status.HTTP_400_BAD_REQUEST       
        return Response({"message":message, "status_code":status_code })
      