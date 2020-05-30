from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from hr.serializers import ListEmployeeSerializer
from django.contrib.auth import get_user_model

EMPLOYEES_LIST = ('/employees/')
EMPLOYEES_HIRE = ('/employees/hire')

class EmployeesTests(TestCase):
    """Tests related to employees"""

    def setUp(self):
        self.client = Client()
        employee = get_user_model().objects.create_user(
            name = 'John Ribbon',
            email = 'john@company.com',
            password = 'johnribbon',
            position = 'manager',
        )
        self.client.force_login(employee)

    def test_add_new_employee(self):
        """Tests successful creation of new employee"""
        employee = get_user_model().objects.create_user(
            name = 'John Ribbon',
            email = 'john@company1.com',
            password = 'johnribbon',
            position = 'manager',
        )

    def test_base_salary_automatically_added(self):
        employee = get_user_model().objects.create_user(
            name = 'John Ribbon',
            email = 'john@company2.com',
            password = 'johnribbon',
            position = 'manager',
        )
        self.assertNotEqual(employee.base_salary, 0)

    def test_retrieve_employees_list(self):
        """Returns a list of all employees of the company"""

        response = self.client.get(EMPLOYEES_LIST)
        employees = get_user_model().objects.all()
        serializer = ListEmployeeSerializer(employees, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_non_hr_user_cannot_hire(self):
        payload = {
            'name': 'John Ribbon',
            'email': 'john@company2.com',
            'password': 'johnribbon',
            'position': 'manager',
        }

        response = self.client.post(EMPLOYEES_HIRE, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
