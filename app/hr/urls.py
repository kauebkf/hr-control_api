from django.urls import path, include
from .views import EmployeesListView

app_name = 'hr'

urlpatterns = [
    path('employees/', EmployeesListView.as_view(), name='employees-list'),

]
