from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from hr.serializers import EmployeeListSerializer
from django.contrib.auth import get_user_model

EMPLOYEES_LIST = ('/employees/')

class EmployeesTests(TestCase):
    """Tests related to employees"""

    def setUp(self):
        self.client = Client()

    def test_add_new_employee(self):
        """Tests successful creation of new employee"""
        employee = get_user_model().objects.create_user(
            name = 'John Ribbon',
            email = 'john@company.com',
            password = 'johnribbon',
            position = 'manager',
        )

    def test_retrieve_employees_list(self):
        """Returns a list of all employees of the company"""

        response = self.client.get(EMPLOYEES_LIST)
        employees = get_user_model().objects.all()
        serializer = EmployeeListSerializer(employees, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)
