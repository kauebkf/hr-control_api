from django.urls import path, include
from .views import EmployeesListView, HireEmployeeView

app_name = 'hr'

urlpatterns = [
    path('employees/', EmployeesListView.as_view(), name='employees-list'),
    path('employees/hire', HireEmployeeView.as_view(), name='employees-hire'),

]
