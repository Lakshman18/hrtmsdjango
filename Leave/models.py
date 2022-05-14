from django.db import models
from Employee.models import Employee

# Create your models here.
class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leaveFromDate = models.DateField()
    leaveToDate = models.DateField()
    reason = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default='pending')
    createdDate = models.DateField(auto_now_add=True)
    modifiedBy = models.CharField(max_length=255, null=True) 
    modifiedDate = models.DateField(auto_now=True, null=True)