from rest_framework.views import APIView
from .serializers import VacancySerializer,ApplicationSerializer
from rest_framework.response import Response
from .models import Vacancy, Applications
from Employee.views import checkEmpRole
from Employee.models import Employee
from Employee.serializers import EmployeeSerializer
from rest_framework import status

# Create your views here.

class vacancy(APIView):
    def get(self, request):
        try:
            # token = checkEmpRole(request.data['token'])
            token = checkEmpRole(request.GET["token"])

            if(token['userRole_name'] == 'admin' ):
                try:
                    my_leave_count = Employee.objects.filter(id = token['id']).values('availableAnnualLeave', 'availableCasualLeave', 'availableSickLeave').first()

                    vacancy = Vacancy.objects.all()
                    vacancy_data = VacancySerializer(vacancy, many=True)
                    message=vacancy_data.data
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
            
            if(token['userRole_name'] == 'admin' ):
                vacancy = Vacancy.objects.filter(department=request.data['department'], designation=request.data['designation'], closingDate__gte =request.data['closingDate']).first()

                if(vacancy):
                    message ="You have already an vacancy."
                    status_code =status.HTTP_400_BAD_REQUEST
                else:  
                    try:                          
                        vacancySerializer = VacancySerializer(data = request.data , partial=True)
                        vacancySerializer.is_valid(raise_exception=True)
                        vacancySerializer.save()
                        message ="New vacancy created successfully"        
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
                    vacancy = Vacancy.objects.filter(id=request.data['id']).first()
                    if(vacancy):
                        vacancySerializer = VacancySerializer(vacancy, data = request.data, partial=True)
                        if vacancySerializer.is_valid(raise_exception=True):
                            message="Edit successful"
                            status_code =status.HTTP_200_OK
                            vacancySerializer.save() 
                        else:
                            message="An Error Occured"
                            status_code =status.HTTP_400_BAD_REQUEST
                    else:
                        message="No matching record found!"
                        status_code =status.HTTP_400_BAD_REQUEST
                except Exception as e:
                    print(e)
                    message ="An Error Occured. Please check the input values"
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
            
            if(token['userRole_name'] == 'admin' ):
                vacancy = Vacancy.objects.filter(id=token['id']).first()
                
                if(vacancy  ):
                    try:                        
                        Vacancy.objects.filter(id=request.data['id']).delete()
                        message="Record has been deleted"
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
        except Exception as e:
            print(e)
            message= "Access denied! Key Missing"  
            status_code =status.HTTP_400_BAD_REQUEST
        return Response({"message":message, "status_code":status_code })


class application(APIView):
    def get(self, request):
        try:
            # token = checkEmpRole(request.data['token'])
            token = checkEmpRole(request.GET["token"])

            if(token['userRole_name'] == 'admin' ):
                try:
                    application = Applications.objects.all()
                    application_data = ApplicationSerializer(application, many=True)
                    message=application_data.data
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


    def put (self, request):
        try:
            token = checkEmpRole(request.data['token'] )
            
            if(token['userRole_name'] == 'admin') :
                try:
                    application = Applications.objects.filter(id=request.data['id']).first()
                    if(application):
                        applicationSerializer = ApplicationSerializer(application, data = request.data, partial=True)
                        if applicationSerializer.is_valid(raise_exception=True):
                            message="Edit successful"
                            status_code =status.HTTP_200_OK
                            applicationSerializer.save() 
                        else:
                            message="An Error Occured"
                            status_code =status.HTTP_400_BAD_REQUEST
                    else:
                        message="No matching record found!"
                        status_code =status.HTTP_400_BAD_REQUEST
                except Exception as e:
                    print(e)
                    message ="An Error Occured. Please check the input values"
                    status_code =status.HTTP_400_BAD_REQUEST

            else:
                message= "Access denied!"    
                status_code =status.HTTP_400_BAD_REQUEST
        except :
            message= "Access denied! Key Missing"  
            status_code =status.HTTP_400_BAD_REQUEST

        return Response({"message":message, "status_code":status_code })
