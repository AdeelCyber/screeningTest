from rest_framework import serializers

from ..models import *


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Application Serializer

    Model: Application

    Fields:
        id: IntegerField
        name: CharField
        description: CharField
        logo: ImageField
        is_active: BooleanField


    """
    class Meta:
        model = Application
        fields = "__all__"
        extra_kwargs = {
            "name": {"required": True, "allow_null": False},
            "description": {"required": True, "allow_null": False},
            "logo": {"required": True, "allow_null": False},
            "is_active": {"required": True, "allow_null": False},
        }

    def create(self, validated_data):
        return Application.objects.create(**validated_data)

