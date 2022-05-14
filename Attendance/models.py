from ast import Delete
from django.db import models
from Employee.models import Employee

# Create your models here.

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    inTime = models.TimeField(auto_now_add=True)
    outTime = models.TimeField(auto_now_add=False, auto_now=False, null=True)