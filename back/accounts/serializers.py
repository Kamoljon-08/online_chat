from rest_framework import generics, permissions
from rest_framework import serializers
from django import forms
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
from django.db.models import Q

# from django.contrib.auth.models import User
from .models import UserModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'username', 'email')

class UserSerializerAll(serializers.ModelSerializer):
    class Meta: 
        model = UserModel
        fields = "__all__"



class RegisterSerializer(serializers.ModelSerializer):
    # password2 = serializers.Password(write_only=True)
    password = serializers.CharField(min_length=12, max_length=16,write_only=True)
    confirm_password = serializers.CharField(min_length=12, max_length=16,write_only=True)
    email = serializers.EmailField(required=True, min_length=7, max_length=30, write_only=True, validators=[UniqueValidator(queryset=UserModel.objects.all(), message="This is email already created")])
    username = serializers.CharField(required=True, min_length=6, max_length=15, write_only=True, validators=[UniqueValidator(queryset=UserModel.objects.all(), message="This is username already created")])

    class Meta:
        model = UserModel
        extra_kwargs = {'password': {'write_only': True}, 'confirm_password':{'write_only': True}}
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password', 'confirm_password')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"error":"Those passwords don't match."})
        return data

    def create(self, validated_data):
        user = UserModel.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            last_name=validated_data['last_name'],
            first_name=validated_data['first_name'],
            password=make_password(validated_data['password'])
        )
        return user

class ChangePasswordSerializer(serializers.Serializer):
    model = UserModel

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)    