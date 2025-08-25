from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'password', 'is_customer', 'is_kitchen', 'is_delivery_agent']
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data.get('phone'),
            is_customer=validated_data.get('is_customer', False),
            is_kitchen=validated_data.get('is_kitchen', False),
            is_delivery_agent=validated_data.get('is_delivery_agent', False),
            password=validated_data['password']
        )
        return user