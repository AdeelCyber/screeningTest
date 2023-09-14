from rest_framework import serializers

from ..models import *


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = "__all__"

    def create(self, validated_data):
        return Subscriptions.objects.create(**validated_data)