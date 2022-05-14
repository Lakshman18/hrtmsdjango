from email.policy import default
from msilib.schema import Class
from django.db import models
from django.contrib.auth.models import AbstractUser
from Department.models import Department
from Designation.models import Designation
# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)  
    isActive = models.BooleanField(default=True)
    createdBy = models.CharField(max_length=255, null=True)
    createdDate = models.DateField(auto_now_add=True, null=True)
    modifiedBy = models.CharField(max_length=255, null=True) 
    modifiedDate = models.DateField(auto_now=True, null=True)

def nameFile(instance, filename):
    return '/'.join(['images', str(instance.firstName + ' ' + instance.lastName), filename])

class Employee(AbstractUser):
    username  = None
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    userRole = models.ForeignKey(Role, on_delete=models.CASCADE)
    nic = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    manager = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    dateOfJoining = models.DateField()
    phoneNumber = models.CharField(max_length=255)
    dob = models.DateField()
    gender = models.CharField(max_length=255, default="Male")
    emergencyContact = models.CharField(max_length=255, null=True)
    religion = models.CharField(max_length=255)
    maritualStatus = models.CharField(max_length=255)
    isActive = models.BooleanField(default=True)
    availableAnnualLeave = models.IntegerField(default=14)
    availableCasualLeave = models.IntegerField(default=14)
    availableSickLeave = models.IntegerField(default=7)
    image = models.ImageField(upload_to=nameFile, blank=True, null=True)
    address = models.CharField(max_length=255)
    createdBy = models.CharField(max_length=255)
    createdDate = models.DateField(auto_now_add=True)
    modifiedBy = models.CharField(max_length=255, null=True) 
    modifiedDate = models.DateField(auto_now=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []