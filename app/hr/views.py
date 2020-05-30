from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from .serializers import EmployeeListSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, mixins


class EmployeesListView(ListAPIView):
    """Lists and retrieves Employee objects"""
    queryset = get_user_model().objects.all()
    serializer_class = EmployeeListSerializer
