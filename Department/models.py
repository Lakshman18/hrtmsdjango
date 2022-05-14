from django.db import models

# Create your models here.

class Department(models.Model):
    departmentName = models.CharField(max_length=255)
    isActive = models.BooleanField(default=True)
    createdBy = models.CharField(max_length=255)
    createdDate = models.DateField(auto_now_add=True)
    modifiedBy = models.CharField(max_length=255) 
    modifiedDate = models.DateField(auto_now=True)