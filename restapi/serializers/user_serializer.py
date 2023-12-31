import re

from rest_framework import serializers

from .application_serializer import ApplicationSerializer
from ..models import *

class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer

    Model: Users

    Fields:
        id: IntegerField
        email: EmailField
        password: CharField
        roles: CharField
        Name: CharField
        username: CharField
        date_joined: DateTimeField
        is_active: BooleanField

    """
    class Meta:
        model = Users
        fields = ['id', 'email', 'password', 'roles', 'Name', "username", "date_joined", "is_active"]


class AppUserSerializer(serializers.ModelSerializer):
    """
        User Serializer

        Model: Users

        Fields:
            id: IntegerField
            email: EmailField
            password: CharField
            roles: CharField
            Name: CharField
            username: CharField
            date_joined: DateTimeField
            is_active: BooleanField
            application: Application

    usage:
    - Login Profile DATA
    - Create Profile DATA
    - Update Profile DATA
    - Delete Profile DATA


    """

    roles = serializers.CharField(required=True)
    Name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True, allow_null=False)
    date_joined = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)
    appDetails = serializers.SerializerMethodField(read_only=True)
    appID = serializers.IntegerField(write_only=True)

    def validate_email(self, value):
        lower_email = value.lower()
        if Users.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Email already exists")
        return lower_email

    def get_appDetails(self, obj):
        user=  ApplicationUsers.objects.filter(id=obj.id).values("application")
        appID = user[0]["application"]
        print(appID)
        application = Application.objects.get(id=appID)
        serializer = ApplicationSerializer(application)
        return serializer.data

    def get_date_joined(self, obj):
        return obj.date_joined.strftime("%b %d, %Y @ %I:%M %p")

    class Meta:
        model = ApplicationUsers
        fields = ['id', 'email', 'password', 'roles', 'Name', "username","appDetails", "date_joined", "is_active","appID"]
        extra_kwargs = {'password': {'write_only': True, 'required': True},
                        "username": {"required": True, "allow_null": False},
                        }

    def create(self, validated_data):

        applicationID = validated_data.pop("appID")
        application = Application.objects.get(id=applicationID)
        user = ApplicationUsers.objects.create_user(application=application, **validated_data)
        return user

    def update(self, instance, validated_data):
        instance.Name = validated_data.get('Name', instance.Name)

        if validated_data.get('password', None):
            instance.set_password(validated_data.get('password'))
        instance.save()
        return instance
