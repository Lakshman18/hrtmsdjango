from asyncio.windows_events import NULL
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import AttendanceSerializer
from rest_framework.response import Response
from .models import Attendance
from Leave.models import Leave
from Employee.models import Employee
from Employee.views import checkEmpRole
from datetime import date,datetime
from rest_framework import status

# Create your views here.

class attendance(APIView):
    def get(self,request):
        try:
            # token = checkEmpRole(request.data['token'])
            token = checkEmpRole(request.GET["token"])
            todays_date = date.today()
            currentMonth =todays_date.month
            
            if(token['userRole_name'] == 'admin' ):
                try:
                    my_attendance = Attendance.objects.filter(employee = token['id']).filter(date__month = currentMonth)
                    my_attendance_data = AttendanceSerializer(my_attendance, many=True)

                    others_attendance = Attendance.objects.exclude(employee = token['id']).filter(date__month = currentMonth)
                    others_attendance_data = AttendanceSerializer(others_attendance, many=True)

                    message = {"my_attendance":my_attendance_data.data, "others_attendance":others_attendance_data.data}
                    status_code =status.HTTP_200_OK
                except:
                    message="An error Occured. Please try again"
                    status_code =status.HTTP_400_BAD_REQUEST

            elif (token['userRole_name'] == 'manager'):
                try:                    
                    my_attendance = Attendance.objects.filter(employee = token['id']).filter(date__month = currentMonth)
                    my_attendance_data = AttendanceSerializer(my_attendance, many=True)

                    my_emp = Employee.objects.filter(manager = token['id']).values('id')

                    others_attendance = Attendance.objects.filter(employee__in = my_emp).filter(date__month = currentMonth)
                    others_attendance_data = AttendanceSerializer(others_attendance, many=True)
                   
                    message = {"my_attendance":my_attendance_data.data, "others_attendance":others_attendance_data.data}
                    status_code =status.HTTP_200_OK
                except Exception as e:
                    print(e)
                    message="An error Occured. Please try again"
                    status_code =status.HTTP_400_BAD_REQUEST
            
            elif (token['userRole_name'] == 'employee'):
                try:
                    my_attendance = Attendance.objects.filter(employee = token['id']).filter(date__month = currentMonth)
                    my_attendance_data = AttendanceSerializer(my_attendance, many=True)
                    status_code =status.HTTP_200_OK
                    message = {"my_attendance":my_attendance_data.data, "others_attendance":{}}
                    
                except Exception as e:
                    print(e)
                    message="An error Occured. Please try again"
                    status_code =status.HTTP_400_BAD_REQUEST
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
            today = date.today()
            request.data['employee']=token['id']
            
            if(token['email'] == request.data['employee_email'] ):
                attendance = Attendance.objects.filter(date=today).filter(employee=token['id']).first()
                leave = Leave.objects.filter(employee=token['id']).filter( status="approved",leaveToDate__gt=today, leaveFromDate__lte=today).first()

                if(attendance):
                    message ="You have already checked in"
                    status_code =status.HTTP_400_BAD_REQUEST
                else:  
                    if(leave):
                        message ="You are on leave today!"
                        status_code =status.HTTP_400_BAD_REQUEST
                    else:
                        try:                          
                            attendanceSerializer = AttendanceSerializer(data = request.data , partial=True)
                            attendanceSerializer.is_valid(raise_exception=True)
                            attendanceSerializer.save()
                            message ="Attendance marked successfully"  
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
            today = date.today()
            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")
            request.data['employee']=token['id']
            request.data['outTime']=current_time
            
            if(token['email'] == request.data['employee_email'] ): 
                attendance = Attendance.objects.filter(date=today).filter(employee=token['id']).first()
                if(attendance):
                    print(attendance.outTime)
                    if(attendance.inTime and attendance.outTime is None ):
                        try:
                            attendanceSerializer = AttendanceSerializer(attendance, data = request.data, partial=True)
                            if attendanceSerializer.is_valid():
                                message="Attendance marked successfully"
                                status_code =status.HTTP_200_OK
                                attendanceSerializer.save() 
                            else:
                                message="You have not checked in today" 
                                status_code =status.HTTP_400_BAD_REQUEST
                        except Exception as e:
                            print(e)
                            message ="An Error Occured. Please check the input values" 
                            status_code =status.HTTP_400_BAD_REQUEST

                    else:
                        message="You have checked out already"   
                        status_code =status.HTTP_400_BAD_REQUEST                           
                else:
                    message="You have not checked in today"  
                    status_code =status.HTTP_400_BAD_REQUEST 
            else:
                message= "Access denied!"   
                status_code =status.HTTP_400_BAD_REQUEST
        except Exception as e:
            print(e)
            message= "Access denied! Key Missing"
            status_code =status.HTTP_400_BAD_REQUEST
        return Response({"message":message, "status_code":status_code })
