from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import serializers


class EmployeeListSerializer(serializers.ModelSerializer):
    """Serializer for Employee model"""
    #  class Salaries(models.IntegerChoices):
    #     director = 5000
    #     manager = 2000
    #     officer = 1500
    #
    # base_salary = models.IntegerField(choices=Salaries.choices)

    class Meta:
        model = get_user_model()
        fields = ('id', 'name', 'position')
