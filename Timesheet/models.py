from django.db import models
from Project.models import Project
from Employee.models import Employee

# Create your models here.
class Timesheet(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateField(null=False, auto_now_add=True)
    startTime = models.TimeField()
    endTime = models.TimeField()
    activity = models.CharField(max_length=255)
