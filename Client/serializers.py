from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'email', 'userRole_name', 'phone', 'dateJoined', 'isActive','taxNo', 'address', 'createdBy', 'createdDate', 'modifiedBy', 'modifiedDate']

        extra_kwargs = {
            'password':{'write_only':True}
        }