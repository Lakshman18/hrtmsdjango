from email.policy import EmailPolicy
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date,datetime
from datetime import date, timedelta
from django.db.models import  Count, CharField, Value
import calendar

from Employee.models import Employee
from Attendance.models import Attendance
from Employee.serializers import EmployeeSerializer
from Project.serializers import ProjectSerializer
from Leave.models import Leave
from Project.models import Project
from NoticeBoard.models import NoticeBoard

from Employee.views import checkEmpRole

from Attendance.serializers import AttendanceSerializer
from rest_framework import status
from django.db.models.functions import Concat


# Create your views here.

class dashboard(APIView):
    def get(self,request):
        try:
            # token = checkEmpRole(request.GET["token"])
            token = checkEmpRole(request.GET["token"])
            
            if(token['userRole_name'] == 'admin' ):
                try:
                    todays_date = date.today()
                    currentMonth =todays_date.month

                    total_employees = Employee.objects.filter(isActive=1).count()
                    today_present_employees = Attendance.objects.filter(date = todays_date).count()

                    today_leave_employees = Leave.objects.filter(leaveToDate__gt=todays_date, leaveFromDate__lte=todays_date, status="approved" ).count()
                    today_absent_employees = total_employees - today_present_employees - today_leave_employees
                    
                    today_my_attendance = Attendance.objects.filter(date = todays_date).filter(employee=token['id']).first()
                    today_my_attendance = AttendanceSerializer(today_my_attendance).data

                    today_employees = Attendance.objects.filter(date = todays_date)
                    today_employees = AttendanceSerializer(today_employees, many=True).data

                    employee_birthday = Employee.objects.filter(dob__month=currentMonth).filter(isActive=1).values('id','firstName', 'lastName', 'dob')
                   
                    notice = NoticeBoard.objects.filter(noticeDate__month = currentMonth).filter(isShow=1).values('id','noticeTitle', 'description')
                    
                    last_30days_present = Attendance.objects.all().values('date').annotate(total=Count('date')).order_by('-date')[:30][::-1]

                    message = {"total_employees":total_employees, "today_present_employees":today_present_employees, 
                                "today_leave_employees":today_leave_employees, "today_absent_employees":today_absent_employees,
                                "today_employees":today_employees, "employee_birthday":employee_birthday,
                                "notice":notice, "last_30days_present":last_30days_present, "today_my_attendance":today_my_attendance}
                    status_code =status.HTTP_200_OK
                except Exception as e:
                    print(e)
                    message="An error Occured. Please try again"
                    status_code =status.HTTP_400_BAD_REQUEST

            elif(token['userRole_name'] == 'manager' or token['userRole_name'] == 'employee' ):
                try:
                    todays_date = date.today()
                    currentMonth =todays_date.month

                    total_employees = Employee.objects.filter(isActive=1).count()

                    employee = Employee.objects.filter(id = token['id']).first()
                    total_leave = employee.availableAnnualLeave + employee.availableCasualLeave + employee.availableSickLeave
                    
                    employee_birthday = Employee.objects.filter(dob__month=currentMonth).filter(isActive=1).values('id','firstName', 'lastName', 'dob')
                   
                    notice = NoticeBoard.objects.filter(noticeDate__month = currentMonth).filter(isShow=1).values('id','noticeTitle', 'description')
                    
                    today_my_attendance = Attendance.objects.filter(date = todays_date).filter(employee=token['id']).first()
                    today_my_attendance = AttendanceSerializer(today_my_attendance).data

                    today = date.today()
                    start = today - timedelta(days=today.weekday())
                    end = start + timedelta(days=4)

                    weekly_attendance = Attendance.objects.filter(date__gte = start, date__lte = end).filter(employee= token['id'])
                    weekly_attendance = AttendanceSerializer(weekly_attendance, many=True).data
                    weekly_attendance = list(weekly_attendance)

                    delta = end - start                    
                   
                    # for item in weekly_attendance:
                    #     print(item['date'])

                    for day in weekly_attendance:
                        if(type(day['outTime']) == str ):
                            inTime = datetime.strptime(day['inTime'], '%H:%M:%S.%f').time()
                            outTime = datetime.strptime(day['outTime'], '%H:%M:%S').time()
                            worked_hours = datetime.combine(date.min, outTime) - datetime.combine(date.min, inTime)
                            day['worked_hours'] = (worked_hours/60)/60
                            # day['worked_hours_description'] = str(worked_hours)
                        else:
                            day['worked_hours'] = 0

                    weekly_attendance_new=[]

                    for i in range(delta.days + 1):
                        day = start + timedelta(days=i)
                        for item in weekly_attendance:
                            if(item['date'] == str(day) ):
                                weekly_attendance_new.append({'date':calendar.day_name[day.weekday()], 'worked_hours':item['worked_hours'] })
                            else:
                                weekly_attendance_new.append({'date':calendar.day_name[day.weekday()], 'worked_hours':0})

                    my_project = Project.objects.filter(employee=token['id'],isActive=1).count()

                    message = {"total_employees":total_employees, "total_leave":total_leave, "employee_birthday":employee_birthday,
                                "notice":notice,"weekly_attendance":weekly_attendance_new, "today_my_attendance":today_my_attendance,
                                'my_project':my_project }
                    status_code =status.HTTP_200_OK
                except Exception as e:
                    print(e)
                    message="An error Occured. Please try again" 
                    status_code =status.HTTP_400_BAD_REQUEST

            elif(token['userRole_name'] == 'client' ):
                try:
                    my_project = Project.objects.filter(client=token['id'],isActive=True).count()

                    my_project_details = Project.objects.filter(client=token['id'],isActive=True)
                    my_project_details = ProjectSerializer(my_project_details, many=True).data

                    message = {'my_project':my_project,'my_project_details':my_project_details }   
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

class test(APIView):
    def get(self,request):

        print (request.GET["token"])

        try:
            emp = Employee.objects.all()
            emp = EmployeeSerializer(emp, many=True).data
            message = emp
            
        except :
            message= "Access denied! Key Missing"  

        return Response(message)

