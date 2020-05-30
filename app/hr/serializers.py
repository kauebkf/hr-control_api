from django.contrib.auth import get_user_model, authenticate
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


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg  = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
