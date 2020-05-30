from rest_framework.generics import ListAPIView,CreateAPIView
from django.contrib.auth import get_user_model
from .serializers import ListEmployeeSerializer, HireEmployeeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from django.views.generic.edit import CreateView


class EmployeesListView(ListAPIView):
    """Lists and retrieves Employee objects"""
    queryset = get_user_model().objects.all()
    serializer_class = ListEmployeeSerializer


class HireEmployeeView(CreateAPIView):
    serializer_class = HireEmployeeSerializer
    fields = ['name', 'email', 'password', 'position']
