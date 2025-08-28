from rest_framework import serializers
from .models import CustomUser, Link
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'role')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name',''),
            last_name=validated_data.get('last_name','')
        )

class LinkSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Link
        fields = ('id','owner','target_url','short_code','title','is_public','created_at')
        read_only_fields = ('short_code','owner')