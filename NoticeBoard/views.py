from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import NoticeBoardSerializer
from rest_framework.response import Response
from .models import NoticeBoard
from Employee.views import checkEmpRole
from rest_framework import status

# Create your views here.

class noticeboard(APIView):
    def get(self,request):
        try:
            # token = checkEmpRole(request.data['token'])
            token = checkEmpRole(request.GET["token"])
            
            if(token['userRole_name'] == 'admin' ):
                try:
                    noticeboard = NoticeBoard.objects.all()
                    noticeboard_data = NoticeBoardSerializer(noticeboard, many=True)
                    message=noticeboard_data.data
                    status_code =status.HTTP_200_OK  
                except Exception as e:
                    print(e)
                    message="An error Occured. Please try again" 
                    status_code =status.HTTP_400_BAD_REQUEST
            elif(token['userRole_name'] == 'employee' or token['userRole_name'] == 'manager' ):
                try:
                    noticeboard = NoticeBoard.objects.filter(isShow = 1)
                    noticeboard_data = NoticeBoardSerializer(noticeboard, many=True)
                    message=noticeboard_data.data
                    status_code =status.HTTP_200_OK  
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
            
            if(token['userRole_name'] == 'admin' ):
                try:
                    noticeboard = NoticeBoard.objects.filter(noticeType=request.data['noticeType'],noticeTitle=request.data['noticeTitle']).first()
                    if(noticeboard):
                        message ="Notice already exists"
                        status_code =status.HTTP_400_BAD_REQUEST
                    else:              
                        noticeSerializer = NoticeBoardSerializer(data = request.data , partial=True)
                        noticeSerializer.is_valid(raise_exception=True)
                        noticeSerializer.save()
                        message ="Notice created successfully"  
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
            
            if(token['userRole_name'] == 'admin' ):
                try:
                    notice = NoticeBoard.objects.filter(id=request.data['id']).first()
                    if(notice):
                        noticeSerializer = NoticeBoardSerializer(notice, data = request.data, partial=True)
                        if noticeSerializer.is_valid(raise_exception=True):
                            message="Edit successful"
                            status_code =status.HTTP_200_OK  
                            noticeSerializer.save() 
                        else:
                            message="No matching notice found"
                            status_code =status.HTTP_400_BAD_REQUEST  
                    else:
                        message="No matching notice found"
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
