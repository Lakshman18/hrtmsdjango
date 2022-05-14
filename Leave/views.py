from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import LeaveSerializer
from rest_framework.response import Response
from .models import Leave
from Employee.views import checkEmpRole
from Employee.models import Employee
from Employee.serializers import EmployeeSerializer
from datetime import date,datetime
from rest_framework import status

# Create your views here.

class leave(APIView):
    def get(self, request):
        try:
            # token = checkEmpRole(request.data['token'])
            token = checkEmpRole(request.GET["token"])

            if(token['userRole_name'] == 'admin' ):
                try:
                    my_leave_count = Employee.objects.filter(id = token['id']).values('availableAnnualLeave', 'availableCasualLeave', 'availableSickLeave').first()

                    my_leave = Leave.objects.filter(employee = token['id'])
                    my_leave_data = LeaveSerializer(my_leave, many=True)
                    my_leave_data = list(my_leave_data.data)

                    for item in my_leave_data:
                        d0 = datetime.fromisoformat(item["leaveFromDate"]).date()
                        d1 = datetime.fromisoformat(item["leaveToDate"]).date()
                        delta = d1 - d0
                        item["days"] = str(delta)[0]

                    others_leave = Leave.objects.exclude(employee = token['id'])
                    others_leave_data = LeaveSerializer(others_leave, many=True)
                    others_leave_data = list(others_leave_data.data)

                    for item in others_leave_data:
                        d0 = datetime.fromisoformat(item["leaveFromDate"]).date()
                        d1 = datetime.fromisoformat(item["leaveToDate"]).date()
                        delta = d1 - d0
                        item["days"] = str(delta)[0]

                    message = {"my_leave_count":my_leave_count, "others_leave":others_leave_data, "my_leave_data":my_leave_data}
                    status_code =status.HTTP_200_OK
                except Exception as e:
                    print(e)
                    message="An error Occured. Please try again"
                    status_code =status.HTTP_400_BAD_REQUEST
            
            elif (token['userRole_name'] == 'manager'):
                try:
                    my_leave_count = Employee.objects.filter(id = token['id']).values('availableAnnualLeave', 'availableCasualLeave', 'availableSickLeave').first()

                    my_leave = Leave.objects.filter(employee = token['id'])
                    my_leave_data = LeaveSerializer(my_leave, many=True)
                    my_leave_data = list(my_leave_data.data)

                    for item in my_leave_data:
                        d0 = datetime.fromisoformat(item["leaveFromDate"]).date()
                        d1 = datetime.fromisoformat(item["leaveToDate"]).date()
                        delta = d1 - d0
                        item["days"] = str(delta)[0]

                    my_emp = Employee.objects.filter(manager = token['id']).values('id')

                    others_leave = Leave.objects.filter(employee__in = my_emp)
                    others_leave_data = LeaveSerializer(others_leave, many=True)
                    others_leave_data = list(others_leave_data.data)

                    for item in others_leave_data:
                        d0 = datetime.fromisoformat(item["leaveFromDate"]).date()
                        d1 = datetime.fromisoformat(item["leaveToDate"]).date()
                        delta = d1 - d0
                        item["days"] = str(delta)[0]

                    message = {"my_leave_count":my_leave_count, "others_leave":others_leave_data, "my_leave_data":my_leave_data}
                    status_code =status.HTTP_200_OK
                except Exception as e:
                    print(e)
                    message="An error Occured. Please try again"    
                    status_code =status.HTTP_400_BAD_REQUEST    

            elif (token['userRole_name'] == 'employee'):
                try:
                    my_leave_count = Employee.objects.filter(id = token['id']).values('availableAnnualLeave', 'availableCasualLeave', 'availableSickLeave').first()

                    my_leave = Leave.objects.filter(employee = token['id'])
                    my_leave_data = LeaveSerializer(my_leave, many=True)
                    my_leave_data = list(my_leave_data.data)

                    for item in my_leave_data:
                        d0 = datetime.fromisoformat(item["leaveFromDate"]).date()
                        d1 = datetime.fromisoformat(item["leaveToDate"]).date()
                        delta = d1 - d0
                        item["days"] = str(delta)[0]

                    message = {"my_leave_count":my_leave_count, "others_leave":{}, "my_leave_data":my_leave_data}
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
            request.data['employee']=token['id']            
            
            if(token['email'] == request.data['employee_email'] ):
                # leave1 = Leave.objects.filter(employee=token['id']).filter(leaveFromDate__gte=request.data['leaveFromDate']).filter(leaveToDate__lt=request.data['leaveFromDate']).first()
                # leave2 = Leave.objects.filter(employee=token['id']).filter(leaveFromDate__gte=request.data['leaveToDate']).filter(leaveToDate__lt=request.data['leaveToDate']).first()
                leave = Leave.objects.filter(employee=token['id']).filter(leaveToDate__gt=request.data['leaveFromDate'], leaveFromDate__lte=request.data['leaveToDate']).first()
                # leave2 = Leave.objects.filter(employee=token['id']).filter(leaveFromDate__gte=request.data['leaveToDate'], leaveToDate__lte=request.data['leaveToDate']).first()
                print(leave)
                if(leave):
                    message ="You have already applied leave for the mentioned dates."
                    status_code =status.HTTP_400_BAD_REQUEST
                else:  
                    try:                          
                        leaveSerializer = LeaveSerializer(data = request.data , partial=True)
                        leaveSerializer.is_valid(raise_exception=True)
                        leaveSerializer.save()
                        message ="Leave applied successfully"        
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
            token = checkEmpRole(request.data['token'] )
            
            if(token['userRole_name'] == 'admin') :
                try:
                    leave = Leave.objects.filter(id=request.data['id']).first()
                    employee = Employee.objects.filter(email=leave.employee).first()

                    if((leave and employee and leave.status=='pending' and request.data['status']=='approved') or (leave and employee and leave.status=='rejected' and request.data['status']=='approved')):
                        if(leave.reason =='annual'):
                            d0 = leave.leaveFromDate
                            d1 = leave.leaveToDate
                            delta = d1 - d0
                            availableAnnualLeave = employee.availableAnnualLeave - delta.days
                            availableAnnualLeave_data = {"availableAnnualLeave":availableAnnualLeave}                            

                            leaveSerializer = LeaveSerializer(leave, data = request.data, partial=True)
                            employeeSerializer = EmployeeSerializer(employee, data = availableAnnualLeave_data, partial=True)
                            
                            if (leaveSerializer.is_valid() and employeeSerializer.is_valid() and availableAnnualLeave>0 ):
                                message="Edit successful"
                                status_code =status.HTTP_200_OK
                                leaveSerializer.save() 
                                employeeSerializer.save()
                            else:
                                if(availableAnnualLeave<0 ):
                                    message="Exeeded the available annual leave count"
                                    status_code =status.HTTP_400_BAD_REQUEST
                                else:
                                    message="something went wrong"
                                    status_code =status.HTTP_400_BAD_REQUEST    

                        elif(leave.reason =='casual'): 
                            d0 = leave.leaveFromDate
                            d1 = leave.leaveToDate
                            delta = d1 - d0
                            availableCasualLeave = employee.availableCasualLeave - delta.days
                            availableCasualLeave_data = {"availableCasualLeave":availableCasualLeave}                            

                            leaveSerializer = LeaveSerializer(leave, data = request.data, partial=True)
                            employeeSerializer = EmployeeSerializer(employee, data = availableCasualLeave_data, partial=True)
                            
                            if (leaveSerializer.is_valid() and employeeSerializer.is_valid() and availableCasualLeave>0 ):
                                message="Edit successful"
                                status_code =status.HTTP_200_OK
                                leaveSerializer.save() 
                                employeeSerializer.save()
                            else:
                                if(availableCasualLeave<0 ):
                                    message="Exeeded the available casual leave count"
                                    status_code =status.HTTP_400_BAD_REQUEST
                                else:
                                    message="something went wrong"
                                    status_code =status.HTTP_400_BAD_REQUEST  

                        else:        
                            d0 = leave.leaveFromDate
                            d1 = leave.leaveToDate
                            delta = d1 - d0
                            availableSickLeave = employee.availableSickLeave - delta.days
                            availableSickLeave_data = {"availableSickLeave":availableSickLeave}                            

                            leaveSerializer = LeaveSerializer(leave, data = request.data, partial=True)
                            employeeSerializer = EmployeeSerializer(employee, data = availableSickLeave_data, partial=True)
                            
                            if (leaveSerializer.is_valid() and employeeSerializer.is_valid() and availableSickLeave>0 ):
                                message="Edit successful"
                                status_code =status.HTTP_200_OK
                                leaveSerializer.save() 
                                employeeSerializer.save()
                            else:
                                if(availableSickLeave<0 ):
                                    message="Exeeded the sick leave count"
                                    status_code =status.HTTP_400_BAD_REQUEST
                                else:
                                    message="something went wrong"
                                    status_code =status.HTTP_400_BAD_REQUEST  

                    elif(leave and leave.status=='pending' and request.data['status']=='rejected'):
                        leaveSerializer = LeaveSerializer(leave, data = request.data, partial=True)
                            
                        if (leaveSerializer.is_valid() ):
                            message="Edit successful"
                            status_code =status.HTTP_200_OK
                            leaveSerializer.save() 
                        else:
                            message="something went wrong"  
                            status_code =status.HTTP_400_BAD_REQUEST

                    elif(leave and employee and leave.status=='approved' ):
                        if(leave.reason =='annual'):
                            d0 = leave.leaveFromDate
                            d1 = leave.leaveToDate
                            delta = d1 - d0
                            availableAnnualLeave = employee.availableAnnualLeave + delta.days
                            availableAnnualLeave_data = {"availableAnnualLeave":availableAnnualLeave}                            

                            leaveSerializer = LeaveSerializer(leave, data = request.data, partial=True)
                            employeeSerializer = EmployeeSerializer(employee, data = availableAnnualLeave_data, partial=True)
                            
                            if (leaveSerializer.is_valid() and employeeSerializer.is_valid() and availableAnnualLeave>0 ):
                                message="Edit successful"
                                status_code =status.HTTP_200_OK
                                leaveSerializer.save() 
                                employeeSerializer.save()
                            else:
                                if(availableAnnualLeave<0 ):
                                    message="Exeeded the annual leave count"
                                    status_code =status.HTTP_400_BAD_REQUEST
                                else:
                                    message="something went wrong"
                                    status_code =status.HTTP_400_BAD_REQUEST 

                        elif(leave.reason =='casual'): 
                            d0 = leave.leaveFromDate
                            d1 = leave.leaveToDate
                            delta = d1 - d0
                            availableCasualLeave = employee.availableCasualLeave + delta.days
                            availableCasualLeave_data = {"availableCasualLeave":availableCasualLeave}                            

                            leaveSerializer = LeaveSerializer(leave, data = request.data, partial=True)
                            employeeSerializer = EmployeeSerializer(employee, data = availableCasualLeave_data, partial=True)
                            
                            if (leaveSerializer.is_valid() and employeeSerializer.is_valid() and availableCasualLeave>0 ):
                                message="Edit successful"
                                status_code =status.HTTP_200_OK
                                leaveSerializer.save() 
                                employeeSerializer.save()
                            else:
                                if(availableCasualLeave<0 ):
                                    message="Exeeded the casual leave count"
                                    status_code =status.HTTP_400_BAD_REQUEST
                                else:
                                    message="something went wrong"
                                    status_code =status.HTTP_400_BAD_REQUEST 

                        else:        
                            d0 = leave.leaveFromDate
                            d1 = leave.leaveToDate
                            delta = d1 - d0
                            availableSickLeave = employee.availableSickLeave + delta.days
                            availableSickLeave_data = {"availableSickLeave":availableSickLeave}                            

                            leaveSerializer = LeaveSerializer(leave, data = request.data, partial=True)
                            employeeSerializer = EmployeeSerializer(employee, data = availableSickLeave_data, partial=True)
                            
                            if (leaveSerializer.is_valid() and employeeSerializer.is_valid() and availableSickLeave>0 ):
                                message="Edit successful"
                                status_code =status.HTTP_200_OK
                                leaveSerializer.save() 
                                employeeSerializer.save()
                            else:
                                if(availableSickLeave<0 ):
                                    message="Exeeded the sick leave count"
                                    status_code =status.HTTP_400_BAD_REQUEST
                                else:
                                    message="something went wrong"
                                    status_code =status.HTTP_400_BAD_REQUEST 
                                  

                    else:
                        message="No record found"
                        status_code =status.HTTP_400_BAD_REQUEST        


                except Exception as e:
                    print(e)
                    message="An error Occured. Please try again"
                    status_code =status.HTTP_400_BAD_REQUEST

            elif(token['userRole_name'] == 'manager') :
                try:
                    leave = Leave.objects.filter(id=request.data['id']).first()
                    employee = Employee.objects.filter(manager = token['id']).filter(email=leave.employee).first()                    
                    
                    if((leave and employee and leave.status=='pending' and request.data['status']=='approved') or (leave and employee and leave.status=='rejected' and request.data['status']=='approved')):
                        if(leave.reason =='annual'):
                            d0 = leave.leaveFromDate
                            d1 = leave.leaveToDate
                            delta = d1 - d0
                            availableAnnualLeave = employee.availableAnnualLeave - delta.days
                            availableAnnualLeave_data = {"availableAnnualLeave":availableAnnualLeave}                            

                            leaveSerializer = LeaveSerializer(leave, data = request.data, partial=True)
                            employeeSerializer = EmployeeSerializer(employee, data = availableAnnualLeave_data, partial=True)
                            
                            if (leaveSerializer.is_valid() and employeeSerializer.is_valid() and availableAnnualLeave>0 ):
                                message="Edit successful"
                                status_code =status.HTTP_200_OK
                                leaveSerializer.save() 
                                employeeSerializer.save()
                            else:
                                if(availableAnnualLeave<0 ):
                                    message="Exeeded the annual leave count"
                                    status_code =status.HTTP_400_BAD_REQUEST
                                else:
                                    message="something went wrong"
                                    status_code =status.HTTP_400_BAD_REQUEST 

                        elif(leave.reason =='casual'): 
                            d0 = leave.leaveFromDate
                            d1 = leave.leaveToDate
                            delta = d1 - d0
                            availableCasualLeave = employee.availableCasualLeave - delta.days
                            availableCasualLeave_data = {"availableCasualLeave":availableCasualLeave}                            

                            leaveSerializer = LeaveSerializer(leave, data = request.data, partial=True)
                            employeeSerializer = EmployeeSerializer(employee, data = availableCasualLeave_data, partial=True)
                            
                            if (leaveSerializer.is_valid() and employeeSerializer.is_valid() and availableCasualLeave>0 ):
                                message="Edit successful"
                                status_code =status.HTTP_200_OK
                                leaveSerializer.save() 
                                employeeSerializer.save()
                            else:
                                if(availableCasualLeave<0 ):
                                    message="Exeeded the casual leave count"
                                    status_code =status.HTTP_400_BAD_REQUEST
                                else:
                                    message="something went wrong"
                                    status_code =status.HTTP_400_BAD_REQUEST 

                        else:        
                            d0 = leave.leaveFromDate
                            d1 = leave.leaveToDate
                            delta = d1 - d0
                            availableSickLeave = employee.availableSickLeave - delta.days
                            availableSickLeave_data = {"availableSickLeave":availableSickLeave}                            

                            leaveSerializer = LeaveSerializer(leave, data = request.data, partial=True)
                            employeeSerializer = EmployeeSerializer(employee, data = availableSickLeave_data, partial=True)
                            
                            if (leaveSerializer.is_valid() and employeeSerializer.is_valid() and availableSickLeave>0 ):
                                message="Edit successful"
                                status_code =status.HTTP_200_OK
                                leaveSerializer.save() 
                                employeeSerializer.save()
                            else:
                                if(availableSickLeave<0 ):
                                    message="Exeeded the sick leave count"
                                    status_code =status.HTTP_400_BAD_REQUEST
                                else:
                                    message="something went wrong"
                                    status_code =status.HTTP_400_BAD_REQUEST

                    elif(leave and employee and leave.status=='pending' and request.data['status']=='rejected'):
                        leaveSerializer = LeaveSerializer(leave, data = request.data, partial=True)
                            
                        if (leaveSerializer.is_valid() ):
                            message="Edit successful"
                            status_code =status.HTTP_200_OK
                            leaveSerializer.save() 
                        else:
                            message="something went wrong"  
                            status_code =status.HTTP_400_BAD_REQUEST

                    elif(leave and employee and leave.status=='approved' and  request.data['status']=='rejected'):
                        if(leave.reason =='annual'):
                            d0 = leave.leaveFromDate
                            d1 = leave.leaveToDate
                            delta = d1 - d0
                            availableAnnualLeave = employee.availableAnnualLeave + delta.days
                            availableAnnualLeave_data = {"availableAnnualLeave":availableAnnualLeave}                            

                            leaveSerializer = LeaveSerializer(leave, data = request.data, partial=True)
                            employeeSerializer = EmployeeSerializer(employee, data = availableAnnualLeave_data, partial=True)
                            
                            if (leaveSerializer.is_valid() and employeeSerializer.is_valid() and availableAnnualLeave>0 ):
                                message="Edit successful"
                                status_code =status.HTTP_200_OK
                                leaveSerializer.save() 
                                employeeSerializer.save()
                            else:
                                if(availableAnnualLeave<0 ):
                                    message="Exeeded the annual leave count"
                                    status_code =status.HTTP_400_BAD_REQUEST
                                else:
                                    message="something went wrong"
                                    status_code =status.HTTP_400_BAD_REQUEST 

                        elif(leave.reason =='casual'): 
                            d0 = leave.leaveFromDate
                            d1 = leave.leaveToDate
                            delta = d1 - d0
                            availableCasualLeave = employee.availableCasualLeave + delta.days
                            availableCasualLeave_data = {"availableCasualLeave":availableCasualLeave}                            

                            leaveSerializer = LeaveSerializer(leave, data = request.data, partial=True)
                            employeeSerializer = EmployeeSerializer(employee, data = availableCasualLeave_data, partial=True)
                            
                            if (leaveSerializer.is_valid() and employeeSerializer.is_valid() and availableCasualLeave>0 ):
                                message="Edit successful"
                                status_code =status.HTTP_200_OK
                                leaveSerializer.save() 
                                employeeSerializer.save()
                            else:
                                if(availableCasualLeave<0 ):
                                    message="Exeeded the casual leave count"
                                    status_code =status.HTTP_400_BAD_REQUEST
                                else:
                                    message="something went wrong"
                                    status_code =status.HTTP_400_BAD_REQUEST 

                        else:
                            d0 = leave.leaveFromDate
                            d1 = leave.leaveToDate
                            delta = d1 - d0
                            availableSickLeave = employee.availableSickLeave - delta.days
                            availableSickLeave_data = {"availableSickLeave":availableSickLeave}                            

                            leaveSerializer = LeaveSerializer(leave, data = request.data, partial=True)
                            employeeSerializer = EmployeeSerializer(employee, data = availableSickLeave_data, partial=True)
                            
                            if (leaveSerializer.is_valid() and employeeSerializer.is_valid() and availableSickLeave>0 ):
                                message="Edit successful"
                                status_code =status.HTTP_200_OK
                                leaveSerializer.save() 
                                employeeSerializer.save()
                            else:
                                if(availableSickLeave<0 ):
                                    message="Exeeded the sick leave count"
                                    status_code =status.HTTP_400_BAD_REQUEST
                                else:
                                    message="something went wrong"
                                    status_code =status.HTTP_400_BAD_REQUEST 
                    
                    else:
                        message="No record found"  
                        status_code =status.HTTP_400_BAD_REQUEST      


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


    def delete(self, request):
        try:
            token = checkEmpRole(request.data['token'])
            request.data['employee']=token['id']            
            
            if(token['email'] == request.data['employee_email'] ):
                leave = Leave.objects.filter(employee=token['id']).filter(id=request.data['id']).first()
                employee = Employee.objects.filter(email=leave.employee).first()

                if(leave and employee ):
                    try:                        
                        print(leave.reason)
                        d0 = leave.leaveFromDate
                        d1 = leave.leaveToDate
                        delta = d1 - d0

                        todays_date = date.today()

                        if(leave.status == "approved" and leave.leaveFromDate>todays_date):
                            Leave.objects.filter(employee=token['id']).filter(id=request.data['id']).delete()
                            
                            if(leave.reason == "annual"):
                                availableAnnualLeave = employee.availableAnnualLeave + delta.days
                                availableAnnualLeave_data = {"availableAnnualLeave":availableAnnualLeave}                            

                                employeeSerializer = EmployeeSerializer(employee, data = availableAnnualLeave_data, partial=True)
                            
                                if (employeeSerializer.is_valid() and availableAnnualLeave>0 ):
                                    message="Your leave has been canceled"
                                    status_code =status.HTTP_200_OK
                                    employeeSerializer.save()
                                else:
                                    message="something went wrong"
                                    status_code =status.HTTP_400_BAD_REQUEST 

                            elif(leave.reason == "casual"):
                                availableCasualLeave = employee.availableCasualLeave + delta.days
                                availableCasualLeave_data = {"availableCasualLeave":availableCasualLeave}                            

                                employeeSerializer = EmployeeSerializer(employee, data = availableCasualLeave_data, partial=True)
                                
                                if (employeeSerializer.is_valid() and availableCasualLeave>0 ):
                                    message="Your leave has been canceled."
                                    status_code =status.HTTP_200_OK
                                    employeeSerializer.save()
                                else:
                                    message="something went wrong"
                                    status_code =status.HTTP_400_BAD_REQUEST 

                            else:
                                availableSickLeave = employee.availableSickLeave + delta.days
                                availableSickLeave_data = {"availableSickLeave":availableSickLeave}                            

                                employeeSerializer = EmployeeSerializer(employee, data = availableSickLeave_data, partial=True)
                                
                                if (employeeSerializer.is_valid() and availableSickLeave>0 ):
                                    message ="Your leave has been canceled."
                                    status_code =status.HTTP_200_OK
                                    employeeSerializer.save()
                                else:
                                    message="something went wrong"
                                    status_code =status.HTTP_400_BAD_REQUEST 

                        elif(leave.status == "approved" and leave.leaveFromDate<todays_date):
                            message ="You cannot delete this record"
                            status_code =status.HTTP_400_BAD_REQUEST
                        else:
                            Leave.objects.filter(employee=token['id']).filter(id=request.data['id']).delete()
                            message ="Your leave has been canceled."
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
