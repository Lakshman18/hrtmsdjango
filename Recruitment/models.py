from django.db import models

# Create your models here.
from django.db import models
from Department.models import Department
from Designation.models import Designation

# Create your models here.
class Vacancy(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    no_of_vacancy = models.IntegerField()
    closingDate = models.DateField(null=True)
    createdBy = models.CharField(max_length=255)
    createdDate = models.DateField(auto_now_add=True)
    modifiedBy = models.CharField(max_length=255) 
    modifiedDate = models.DateField(auto_now=True)

class Applications(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    applicant_name = models.CharField(max_length=255)
    applicant_email = models.CharField(max_length=255)
    applicant_phone = models.CharField(max_length=255)
    applicant_status = models.CharField(max_length=255)
    applicant_cv = models.CharField(max_length=255)
    createdBy = models.CharField(max_length=255)
    createdDate = models.DateField(auto_now_add=True)
    modifiedBy = models.CharField(max_length=255) 
    modifiedDate = models.DateField(auto_now=True)