from django.urls import path, include
from .views import EmployeesListView, HireEmployeeView, CreateTokenView, \
                    Attendance

app_name = 'hr'

urlpatterns = [
    path('employees/', EmployeesListView.as_view(), name='employees-list'),
    path('employees/hire/', HireEmployeeView.as_view(), name='employees-hire'),
    path('login/', CreateTokenView.as_view(), name='login'),
    path('attend/', Attendance.as_view(), name='attend'),

]
