from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import TimesheetSerializer
from Project.serializers import ProjectSerializer
from rest_framework.response import Response
from .models import Timesheet
from Project.models import Project
from Leave.models import Leave
from Employee.models import Employee
from Employee.views import checkEmpRole
from datetime import date,datetime
from rest_framework import status

# Create your views here.

class timesheet(APIView):
    def get(self,request):
        try:
            # token = checkEmpRole(request.data['token'])
            token = checkEmpRole(request.GET["token"])
            
            if(token['userRole_name'] == 'admin' ):
                try:
                    my_timesheet = Timesheet.objects.filter(employee = token['id'])
                    my_timesheet_data = TimesheetSerializer(my_timesheet, many=True)

                    my_project = Project.objects.filter(employee= token['id']).filter(isActive=True)
                    my_project_data = ProjectSerializer(my_project, many=True).data

                    others_timesheet = Timesheet.objects.exclude(employee = token['id'])
                    others_timesheet_data = TimesheetSerializer(others_timesheet, many=True)

                    message = {"my_project":my_project_data, "others_timesheet":others_timesheet_data.data, "my_timesheet":my_timesheet_data.data}
                    status_code =status.HTTP_200_OK
                except Exception as e:
                    print(e)
                    message="An error Occured. Please try again"
                    status_code =status.HTTP_400_BAD_REQUEST

            elif(token['userRole_name'] == 'manager' ):
                try:
                    my_timesheet = Timesheet.objects.filter(employee = token['id'])
                    my_timesheet_data = TimesheetSerializer(my_timesheet, many=True)

                    my_emp = Employee.objects.filter(manager = token['id']).values('id')

                    others_timesheet = Timesheet.objects.filter(employee__in = my_emp)
                    others_timesheet_data = TimesheetSerializer(others_timesheet, many=True)

                    my_project = Project.objects.filter(employee= token['id']).filter(isActive=True)
                    my_project_data = ProjectSerializer(my_project, many=True).data

                    message = {"my_project":my_project_data, "others_timesheet":others_timesheet_data.data, "my_timesheet":my_timesheet_data.data}
                    status_code =status.HTTP_200_OK
                except Exception as e:
                    print(e)
                    message="An error Occured. Please try again"  
                    status_code =status.HTTP_400_BAD_REQUEST
            elif(token['userRole_name'] == 'employee' ):
                try:
                    my_timesheet = Timesheet.objects.filter(employee = token['id'])
                    my_timesheet_data = TimesheetSerializer(my_timesheet, many=True)

                    my_project = Project.objects.filter(employee= token['id']).filter(isActive=True)
                    my_project_data = ProjectSerializer(my_project, many=True).data

                    message = {"my_project":my_project_data, "others_timesheet":{}, "my_timesheet":my_timesheet_data.data}
                    status_code =status.HTTP_200_OK
                except Exception as e:
                    print(e)
                    message="An error Occured. Please try again"    
                    status_code =status.HTTP_400_BAD_REQUEST

            elif(token['userRole_name'] == 'client' ):
                try:
                    my_project = Project.objects.filter(client = token['id'], isActive=1).values('id')

                    my_timesheet = Timesheet.objects.filter(project__in = my_project)
                    my_timesheet_data = TimesheetSerializer(my_timesheet, many=True)

                    message = {"my_project":my_project, "others_timesheet":{}, "my_timesheet":my_timesheet_data.data}
                    status_code =status.HTTP_200_OK
                except Exception as e:
                    print(e)
                    message="An error Occured. Please try again"    
                    status_code =status.HTTP_400_BAD_REQUEST
                    
            else:
                message= "Access denied!" 
                status_code =status.HTTP_400_BAD_REQUEST   
        except :
            message= "Access denied! Key Missing"  
            status_code =status.HTTP_400_BAD_REQUEST

        return Response({"message":message, "status_code":status_code })

    def post(self, request):
        try:
            token = checkEmpRole(request.data['token']) 
            todays_date = date.today()           
            
            if(token['id'] ):
                request.data['employee'] = token['id']
                timesheet = Timesheet.objects.filter(date=todays_date).filter(project=request.data['project']).filter(employee=token['id'] ).first()
                leave = Leave.objects.filter(employee=token['id']).filter(leaveToDate__gt=todays_date, leaveFromDate__lte=todays_date, status="approved").first()

                if(timesheet):
                    message ="timesheet already exists"
                    status_code =status.HTTP_400_BAD_REQUEST
                else:
                    if(leave):
                        message ="You are on leave today!"
                        status_code =status.HTTP_400_BAD_REQUEST
                    else:
                        try:                          
                            timesheetSerializer = TimesheetSerializer(data = request.data , partial=True)
                            timesheetSerializer.is_valid(raise_exception=True)
                            timesheetSerializer.save()
                            message ="timesheet created successfully"
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
            timesheet = Timesheet.objects.filter(id=request.data['id']).first()
            
            if(str(token['email']) == str(timesheet.employee) ):
                print("in")  
                request.data['employee'] = token['id']      
                
                if(timesheet):
                    print("yes") 
                    try:
                        timesheetSerializer = TimesheetSerializer(timesheet, data = request.data, partial=True)
                        if timesheetSerializer.is_valid():
                            message="Edit successful"
                            status_code =status.HTTP_200_OK
                            timesheetSerializer.save() 
                        else:
                            message="No matching timesheet found" 
                            status_code =status.HTTP_400_BAD_REQUEST
                    except Exception as e:
                        print(e)
                        message ="An Error Occured. Please check the input values"
                        status_code =status.HTTP_400_BAD_REQUEST         
                else:
                    message="No matching timesheet found"   
                    status_code =status.HTTP_400_BAD_REQUEST
            else:
                message= "Access denied!"   
                status_code =status.HTTP_400_BAD_REQUEST
        except:
            message= "Access denied! Key Missing"
            status_code =status.HTTP_400_BAD_REQUEST
        return Response({"message":message, "status_code":status_code })


    def delete(self, request):
        try:
            token = checkEmpRole(request.data['token'])
            # request.data['employee']=token['id']  
            timesheet = Timesheet.objects.filter(employee=token['id']).filter(id=request.data['id']).first()          
            
            if(str(token['email']) == str(timesheet.employee) ):               

                if(timesheet ):
                    try:                   
                        Timesheet.objects.filter(employee=token['id']).filter(id=request.data['id']).delete()
                            
                        message ="Your record has been deleted."
                        status_code =status.HTTP_200_OK
                    except Exception as e:
                        print(e)
                        message ="An Error Occured. Please check the input values"
                        status_code =status.HTTP_400_BAD_REQUEST
                else:  
                    message ="Access denied! No record found"
                    status_code =status.HTTP_400_BAD_REQUEST
            else:
                message= "Access denied!"  
                status_code =status.HTTP_400_BAD_REQUEST  
        except:
            message= "Access denied! Key Missing"  
            status_code =status.HTTP_400_BAD_REQUEST
        return Response({"message":message, "status_code":status_code })

        