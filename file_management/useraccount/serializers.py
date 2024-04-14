
from rest_framework import serializers
from .models import CustomUser

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        
        user = CustomUser.objects.create_owner(**validated_data)
        return user

class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'name', 'is_owner', 'is_staff', 'date_joined')
        read_only_fields = ('id', 'email', 'name', 'is_owner', 'is_staff', 'date_joined')
