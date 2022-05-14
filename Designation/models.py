from django.db import models
from Department.models import Department

# Create your models here.

class Designation(models.Model):
    designationName = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    isActive = models.BooleanField(default=True)
    createdBy = models.CharField(max_length=255)
    createdDate = models.DateField(auto_now_add=True)
    modifiedBy = models.CharField(max_length=255, null=True) 
    modifiedDate = models.DateField(auto_now=True, null=True)