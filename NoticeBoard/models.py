from django.db import models
# Create your models here.

class NoticeBoard(models.Model):
    noticeType = models.CharField(max_length=255)
    noticeTitle = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    noticeDate = models.DateField(null=True)
    isShow = models.CharField(max_length=255)
    createdBy = models.CharField(max_length=255)
    createdDate = models.DateField(auto_now_add=True)
    modifiedBy = models.CharField(max_length=255) 
    modifiedDate = models.DateField(auto_now=True)