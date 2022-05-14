from django.db import models
from Client.models import Client
from Employee.models import Employee

# Create your models here.
class Project(models.Model):
    projectName = models.CharField(max_length=255)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    employee = models.ManyToManyField(Employee)
    startDate = models.DateField(null=True)
    renewalDate = models.DateField(null=True)
    isActive = models.BooleanField(default=True)
    createdBy = models.CharField(max_length=255)
    createdDate = models.DateField(auto_now_add=True)
    modifiedBy = models.CharField(max_length=255) 
    modifiedDate = models.DateField(auto_now=True)
