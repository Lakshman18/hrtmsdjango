from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    dateJoined = models.DateField()    
    userRole_name = models.CharField(max_length=255, default='client')
    isActive = models.BooleanField(default=True)
    taxNo = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    createdBy = models.CharField(max_length=255)
    createdDate = models.DateField(auto_now_add=True)
    modifiedBy = models.CharField(max_length=255) 
    modifiedDate = models.DateField(auto_now=True)