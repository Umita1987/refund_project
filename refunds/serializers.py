from rest_framework import serializers
from .models import RefundRequest

class RefundRequestSerializer(serializers.ModelSerializer):
    # This serializer displays all fields (for viewing and admin editing)
    class Meta:
        model = RefundRequest
        fields = '__all__'


class RefundRequestCreateSerializer(serializers.ModelSerializer):
    # This serializer is used for user creation and editing (fields are hidden)
    class Meta:
        model = RefundRequest
        exclude = ['user', 'status', 'iban_verified']
