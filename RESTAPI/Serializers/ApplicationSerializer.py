from rest_framework import serializers

from ..models import *


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
        extra_kwargs = {
            "name": {"required": True, "allow_null": False},
            "description": {"required": True, "allow_null": False},
            "logo": {"required": True, "allow_null": False},
            "is_active": {"required": True, "allow_null": False},
            "is_deleted": {"required": True, "allow_null": False},
        }

    def create(self, validated_data):
        return Application.objects.create(**validated_data)
