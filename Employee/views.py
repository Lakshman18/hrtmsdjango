from logging import raiseExceptions
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from .serializers import RoleSerializer, EmployeeSerializer
from rest_framework.response import Response
from .models import Role, Employee
from Client.models import Client
from Client.serializers import ClientSerializer
import jwt,datetime
from rest_framework import status
from django.contrib.auth.hashers import make_password


class roles(APIView):
    def get(self,request):
        try:
            # token = checkEmpRole(request.data['token'])            
            token = checkEmpRole(request.GET["token"])

            if(token['userRole_name'] == 'admin' ):
                try:
                    roles = Role.objects.all()
                    roles_data = RoleSerializer(roles, many=True)
                    message = roles_data.data
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
            message= "Access denied, Key Missing!" 
            status_code =status.HTTP_400_BAD_REQUEST 

        return Response({"message":message, "status_code":status_code })

    def post(self, request):
        try:
            token = checkEmpRole(request.data['token'])

            if(token['userRole_name'] == 'admin' ):
                try:
                    role = Role.objects.filter(name=request.data['name']).first()
                    if(role):
                        message ="Role already exists"
                        status_code =status.HTTP_400_BAD_REQUEST
                    else:
                        roleSerializer = RoleSerializer(data = request.data , partial=True)
                        roleSerializer.is_valid(raise_exception=True)
                        roleSerializer.save()
                        message = "Role created successfully"
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
            message= "Access denied, Key Missing!"  
            status_code =status.HTTP_400_BAD_REQUEST
        return Response({"message":message, "status_code":status_code })

    def put (self, request):
        try:
            token = checkEmpRole(request.data['token'])

            if(token['userRole_name'] == 'admin' ):
                try:
                    role = Role.objects.filter(id=request.data['id']).first()

                    if(role):
                        roleSerializer = RoleSerializer(role, data = request.data, partial=True)
                        if roleSerializer.is_valid():
                            message="Edit successful"
                            status_code =status.HTTP_200_OK
                            roleSerializer.save() 
                        else:
                            message="No matching role found"  
                            status_code =status.HTTP_400_BAD_REQUEST
                    else:
                        message="No matching role found"   
                        status_code =status.HTTP_400_BAD_REQUEST
                except Exception as e:
                    print(e)
                    message ="An Error Occured. Please check the input values"
                    status_code =status.HTTP_400_BAD_REQUEST

            else:
                message= "Access denied!"
                status_code =status.HTTP_400_BAD_REQUEST
        except Exception as e:
            print(e)
            message= "Access denied, Key Missing!" 
            status_code =status.HTTP_400_BAD_REQUEST 

        return Response({"message":message, "status_code":status_code })

class Register(APIView):
    def post(self, request):
        try:
            token = checkEmpRole(request.data['token'])

            if(token['userRole_name'] == 'admin'):
                emp = Employee.objects.filter(email = request.data["email"] ).first()
                if(emp is None):
                    try:
                        employeeSerializer = EmployeeSerializer(data = request.data)
                        employeeSerializer.is_valid(raise_exception=True)
                        employeeSerializer.save()
                        message="User registered successfully"  
                        status_code =status.HTTP_200_OK    
                    except Exception as e:
                        print(e)
                        message="Something went wrong" 
                        status_code =status.HTTP_400_BAD_REQUEST    
                else:
                    message="Email already exists"
                    status_code =status.HTTP_400_BAD_REQUEST     
            else:
                message= "Access denied!"  
                status_code =status.HTTP_400_BAD_REQUEST     
        except:
            message= "Access denied, Key Missing!" 
            status_code =status.HTTP_400_BAD_REQUEST     

        return Response({"message":message, "status_code":status_code })

    def put(self, request):
        try:
            token = checkEmpRole(request.data['token'] )

            if(token['userRole_name'] == 'admin'  or request.data["modifiedBy"] == token['email'] ):
                emp = Employee.objects.filter(email = request.data["email"] ).first()
                if(emp ):
                    try:
                        employeeSerializer = EmployeeSerializer(emp, data = request.data, partial=True)
                        if employeeSerializer.is_valid(raise_exception=True):
                            message="Edit successful"
                            status_code =status.HTTP_200_OK  
                            employeeSerializer.save() 
                        else:
                            message="Something went wrong" 
                            status_code =status.HTTP_400_BAD_REQUEST 
                    except Exception as e:
                        print(e)
                        message="Something went wrong" 
                        status_code =status.HTTP_400_BAD_REQUEST  
                else:
                    message="No employee record exists" 
                    status_code =status.HTTP_400_BAD_REQUEST  
            else:
                message= "Access denied!"  
                status_code =status.HTTP_400_BAD_REQUEST  
        except:
            message= "Access denied, Key Missing!"
            status_code =status.HTTP_400_BAD_REQUEST  

        return Response({"message":message, "status_code":status_code })

class Login(APIView):
    def post(self,request):
        try:
            email = request.data['email']
            password = request.data['password']

            emp = Employee.objects.filter(email=email).first()
            empSer = EmployeeSerializer(emp, data = request.data, partial=True)
            
            if emp is None:
                message="User not found"
                status_code =status.HTTP_400_BAD_REQUEST  

            if emp and not emp.check_password(password):
                message="Incorrect password"
                status_code =status.HTTP_400_BAD_REQUEST  

            if (emp and emp.check_password(password) and emp.isActive==True) :
                payload = {
                    'id':emp.id,
                    'userRole':"employee",
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=560),  
                    'iat': datetime.datetime.utcnow()
                } 

                token= jwt.encode(payload,'secret',algorithm='HS256')
                
                response = Response()

                response.set_cookie(key='jwt', value=token, httponly=True)
                response.data= {
                    'jwt':token,
                    'userRole':emp.userRole.name
                }

                message=response.data
                status_code =status.HTTP_200_OK  
        except Exception as e:
            print(e)
            message="Error occured"
            status_code =status.HTTP_400_BAD_REQUEST  

        return Response({"message":message, "status_code":status_code })

#This view is used to view the partcular emloyee own details that who have logged into the system
class EmpView1(APIView):
    def post(self, request):
        try:
            token = request.data['token']

            if not  token:
                message="Unauthenticated"
                status_code =status.HTTP_400_BAD_REQUEST
            else:
                try:
                    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                    user = Employee.objects.filter(id=payload['id']).first()
                    serializer = EmployeeSerializer(user)
                    message=serializer.data
                    status_code =status.HTTP_200_OK

                except Exception as e:
                    message="Unauthenticated"
                    status_code =status.HTTP_400_BAD_REQUEST
        except:
            message= "Access denied! Key Missing" 
            status_code =status.HTTP_400_BAD_REQUEST
        return Response({"message":message, "status_code":status_code })

class EmpView(APIView):
    def post(self, request):
        try:
            token = checkEmpRole(request.data['token'])
            print(token)
            print(token['userRole_name'])
            if(token['userRole_name'] == 'admin' or token['userRole_name'] =='manager' or token['userRole_name'] =='employee' ):
                try:
                    user = Employee.objects.filter(id=token['id']).first()
                    serializer = EmployeeSerializer(user)
                    message=serializer.data
                    status_code =status.HTTP_200_OK

                except Exception as e:
                    message="Unauthenticated"
                    status_code =status.HTTP_400_BAD_REQUEST
            else:
                message="Unauthenticated"
                status_code =status.HTTP_400_BAD_REQUEST   
        except:
            message= "Access denied! Key Missing" 
            status_code =status.HTTP_400_BAD_REQUEST
        return Response({"message":message, "status_code":status_code })

class Logout(APIView):
    def post(self,request):
        try:
            response =Response()
            response.delete_cookie('jwt')
            response.data = {
                'message': 'success'
            }
        except Exception as e:
            response.data = {
                'message': 'failed'
            }
        return response  

class viewAllEmp(APIView):
    def get(self,request):
        try:
            # token = checkEmpRole(request.data['token'])            
            token = checkEmpRole(request.GET["token"])

            if(token['userRole_name'] == 'admin' ):
                try:
                    employee = Employee.objects.all()
                    employee_data = EmployeeSerializer(employee, many=True)
                    message = employee_data.data
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


class PwdChange(APIView):
    def put(self,request):
        try:
            token = checkEmpRole(request.data['token'] )
            email=request.data['email']
            oldPassword=request.data['oldPassword']
            newPassword=request.data['newPassword']

            if(email == token['email']):
                user = Employee.objects.filter(email=email).first()           
                
                if user:
                    if user.check_password(oldPassword):
                        user.password = make_password(newPassword) 
                        user.save()
                        message="Password changed successfully"
                        status_code =status.HTTP_200_OK
                    else:
                        message="Current password is wrong"
                        status_code =status.HTTP_400_BAD_REQUEST
                else :
                    message="User not found"
                    status_code =status.HTTP_400_BAD_REQUEST     
            else:
                message="Access Denied"
                status_code =status.HTTP_400_BAD_REQUEST     

        except Exception as e:
            print(e)
            message="Error occured"
            status_code =status.HTTP_400_BAD_REQUEST       
       
        return Response({"message":message, "status_code":status_code })

class pictureChange(APIView):
    def put(self, request):
        try:
            print(request.data)
            token = checkEmpRole(request.data['token'] )

            if(request.data['modifiedBy'] == token['email']):
                data= request.data        
                emp = Employee.objects.filter(email=token['email']).first()

                file_serializer = EmployeeSerializer(emp, data = request.data, partial=True)
                if file_serializer.is_valid():
                    if emp.image:
                        emp.image.delete()
                        file_serializer.save()  
                        message="Profile Picture changed successfully" 
                        status_code =status.HTTP_200_OK             
                    else:        
                        file_serializer.save()  
                        message="Profile Picture changed successfully"
                        status_code =status.HTTP_200_OK               
                    
                else:
                    message="An error occured"
                    status_code =status.HTTP_400_BAD_REQUEST
            else:
                message="Access Denied"
                status_code =status.HTTP_400_BAD_REQUEST    
        except Exception as e:
            print(e)
            message="Error occured"
            status_code =status.HTTP_400_BAD_REQUEST 

        return Response({"message":message, "status_code":status_code }) 

def checkEmpRole(token):
    if not  token:
        message= {"userRole_name": "Unauthenticated"}
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        if(payload['userRole']=="employee"):
            user = Employee.objects.filter(id=payload['id']).first()
            serializer = EmployeeSerializer(user)
            message=serializer.data
        elif(payload['userRole']=="client"):    
            user = Client.objects.filter(id=payload['id']).first()
            serializer = ClientSerializer(user)
            message=serializer.data
        else:
            message= {"userRole_name": "Unauthenticated"}
    except Exception as e:
        print(e)
        message= {"userRole_name": "Unauthenticated"}

    return message

