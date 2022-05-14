from rest_framework import serializers
from .models import NoticeBoard

class NoticeBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeBoard
        fields = ['id','noticeType', 'noticeTitle', 'description', 'noticeDate', 'isShow', 'createdBy', 'createdDate', 'modifiedBy', 'modifiedDate']
