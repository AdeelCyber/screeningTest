from rest_framework import serializers

from ..models import *


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Subscription Serializer

    Model: Subscriptions

    Fields:
        id: IntegerField
        application: Application
        package: Packages
        date: DateTimeField
        is_active: BooleanField

    """
    class Meta:
        model = Subscriptions
        fields = "__all__"

    def create(self, validated_data):
        return Subscriptions.objects.create(**validated_data)