from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import serializers


class ListEmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee model"""
    net_salary = serializers.DecimalField(
        max_digits=7,
        decimal_places=2,
        )

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'name',
            'position',
            'base_salary',
            'attendance',
            'net_salary'
        )


class HireEmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee model"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'name', 'position', 'email', 'password')

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
