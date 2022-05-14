from encodings import utf_8
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ClientSerializer
from rest_framework.response import Response
from .models import Client as ClientModel
from Employee.views import checkEmpRole
from cryptography.fernet import Fernet
import jwt,datetime
from rest_framework.exceptions import AuthenticationFailed
from cryptography.fernet import Fernet
import base64
from rest_framework import status


# Create your views here.

class Client(APIView):
    def get(self,request):
        try:
            # token = checkEmpRole(request.data['token'])
            token = checkEmpRole(request.GET["token"])
            
            if(token['userRole_name'] == 'admin' ):
                try:
                    client = ClientModel.objects.all()
                    client_data = ClientSerializer(client, many=True)
                    message = client_data.data
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
                client = ClientModel.objects.filter(email=request.data['email']).first()
                if(client):
                    message ="Client already exists"
                    status_code =status.HTTP_400_BAD_REQUEST
                else:
                    try:
                        client_password = request.data['client_password']
                        client_password = base64.b64encode(client_password.encode("utf-8"))
                        newpass = client_password.decode("utf-8")
                        request.data['password'] = newpass

                        clientSerializer = ClientSerializer(data = request.data , partial=True)
                        clientSerializer.is_valid(raise_exception=True)
                        clientSerializer.save()
                        message ="Client created successfully"   
                        status_code =status.HTTP_200_OK
                    except Exception as e:   
                        print(e)
                        message ="An Error Occured."  
                        status_code =status.HTTP_400_BAD_REQUEST

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

            if(token['userRole_name'] == 'admin' or (token['userRole_name'] == 'client' and request.data['modifiedBy'] == token['email']) ):
                client = ClientModel.objects.filter(email = request.data["email"] ).first()
                if(client ):
                    try:
                        clientSerializer = ClientSerializer(client, data = request.data, partial=True)
                        if clientSerializer.is_valid():
                            message="Edit successful"
                            status_code =status.HTTP_200_OK
                            clientSerializer.save() 
                    except Exception as e:
                        print(e)
                        message="Something went wrong" 
                        status_code =status.HTTP_400_BAD_REQUEST
                else:
                    message="No client record exists" 
                    status_code =status.HTTP_400_BAD_REQUEST
            else:
                message= "Access denied!"   
                status_code =status.HTTP_400_BAD_REQUEST
        except Exception as e:
            print(e)
            message= "Access denied, Key Missing!"  
            status_code =status.HTTP_400_BAD_REQUEST

        return Response({"message":message, "status_code":status_code })


class Login(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            client_password = request.data['password']

            client_password = base64.b64encode(client_password.encode("utf-8"))
            decryptedPass = client_password.decode("utf-8")

            client = ClientModel.objects.filter(email=email).first()
            
            if client is None:
                message="User not found"
                status_code =status.HTTP_400_BAD_REQUEST
            
            actualClient = ClientModel.objects.filter(email=email).filter(password=decryptedPass).first()

            if client and not actualClient:
                message="Incorrect password"
                status_code =status.HTTP_400_BAD_REQUEST  
            
            if client and  actualClient:
                payload = {
                    'id':actualClient.id,
                    'userRole':"client",
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=560),  
                    'iat': datetime.datetime.utcnow()
                } 

                token= jwt.encode(payload,'secret',algorithm='HS256')
                
                response = Response()

                response.set_cookie(key='jwt', value=token, httponly=True)
                response.data= {
                    'jwt':token,
                    'userRole':"client",
                }

                message=response.data
                status_code =status.HTTP_200_OK  

        except Exception as e:
            print(e)
            message="Error occured"
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
                user = ClientModel.objects.filter(email=email).first()        
                
                if user:                      
                    client_password = base64.b64encode(oldPassword.encode("utf-8"))
                    decryptedPass = client_password.decode("utf-8") 

                    actualClient = ClientModel.objects.filter(email=email).filter(password=decryptedPass).first()

                    if actualClient:
                        new_client_password = base64.b64encode(newPassword.encode("utf-8"))
                        newpass = new_client_password.decode("utf-8")
                        actualClient.password = newpass
                        actualClient.save()
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


class ClientView(APIView):
    def post(self, request):
        try:
            token = checkEmpRole(request.data['token'])
            if(token['userRole_name'] == 'client'):
                try:
                    user = ClientModel.objects.filter(id=token['id']).first()
                    serializer = ClientSerializer(user)
                    message=serializer.data
                    status_code =status.HTTP_200_OK

                except Exception as e:
                    print(e)
                    message="Unauthenticated"
                    status_code =status.HTTP_400_BAD_REQUEST   
            else:
                message="Unauthenticated"
                status_code =status.HTTP_400_BAD_REQUEST   
        except:
            message= "Access denied! Key Missing" 
            status_code =status.HTTP_400_BAD_REQUEST
        return Response({"message":message, "status_code":status_code })