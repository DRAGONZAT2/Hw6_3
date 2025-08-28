from rest_framework import serializers
from .models import CustomUser, Note
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer




class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CustomUser
        fields = ('id','email','first_name','last_name','role')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = CustomUser
        fields = ('email','password','first_name','last_name', 'role')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name',''),
            last_name=validated_data.get('last_name',''),
            role=validated_data.get('role', 'user')
        
        )
        user.save()
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
        @classmethod
        def get_token(cls, user):
            token = super().get_token(user)
            token["role"] = user.role
            token["email"] = user.email
            return token

        def validate(self, attrs):
            data = super().validate(attrs)
            user = self.user
            data["user"] = {
            "id": user.id,
            "email": user.email,
            "role": user.role,
        }
            return data
        

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'role')
        
class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.email')

    class Meta:
        model = Note
        fields = '__all__'