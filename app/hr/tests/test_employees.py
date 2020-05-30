from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from hr.serializers import ListEmployeeSerializer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

EMPLOYEES_LIST = ('/employees/')
EMPLOYEES_HIRE = ('/employees/hire/')
ATTEND = ('/attend/')

class EmployeesTests(TestCase):
    """Tests related to employees"""

    def setUp(self):
        self.client = APIClient()
        employee = get_user_model().objects.create_user(
            name = 'John Ribbon',
            email = 'john@company.com',
            password = 'johnribbon',
            position = 'manager',
        )
        self.client.force_authenticate(employee)

    def test_add_new_employee(self):
        """Tests successful creation of new employee using custom fields"""
        employee = get_user_model().objects.create_user(
            name = 'John Ribbon',
            email = 'john@company1.com',
            password = 'johnribbon',
            position = 'manager',
        )

    def test_base_salary_automatically_added(self):
        """Tests automatic assignment of base salary"""
        employee = get_user_model().objects.create_user(
            name = 'John Ribbon',
            email = 'john@company2.com',
            password = 'johnribbon',
            position = 'manager',
        )
        self.assertNotEqual(employee.base_salary, 0)


    def test_non_hr_user_cannot_hire(self):
        """Tests that non hr managers cannot hire"""
        payload = {
            'name': 'John Ribbon',
            'email': 'john@company2.com',
            'password': 'johnribbon',
            'position': 'manager',
        }

        response = self.client.post(EMPLOYEES_HIRE, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_daily_attendance_works(self):
        """Tests that attendance field value increases when hitting endpoint"""
        client = APIClient()
        employee = get_user_model().objects.create_user(
            name = 'Mark Edwards',
            email = 'mark2@edwards.com',
            password = 'markedwards',
            position = 'director',
        )
        self.assertEqual(employee.attendance, 0)
        client.force_authenticate(employee)
        response = client.get(ATTEND)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(employee.attendance, 1)

    def test_daily_attendance_limit(self):
        """Tests that user can attend only once per day"""
        response1 = self.client.get(ATTEND)
        response2 = self.client.get(ATTEND)

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(
        response2.status_code,
        status.HTTP_429_TOO_MANY_REQUESTS
        )


class HRTests(TestCase):
    """Tests for the hr manager"""

    def setUp(self):
        employee = get_user_model().objects.create_user(
            name = 'Hr Admin',
            email = 'hradmin@company.com',
            password = 'hradmin',
            position = 'director',
        )
        self.client = APIClient()

        self.client.force_authenticate(employee)

    def test_retrieve_employees_list(self):
        """Returns a list of all employees of the company"""

        response = self.client.get(EMPLOYEES_LIST)
        employees = get_user_model().objects.all()
        serializer = ListEmployeeSerializer(employees, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_hire_new_employee(self):
        """Test hiring new employee using endpoint"""
        payload = {
            'name': 'Robert Peterson',
            'email': 'robert@peterson.com',
            'password': 'robertpeterson',
            'position': 'officer'
        }
        response = self.client.post(EMPLOYEES_HIRE, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        employee = get_user_model().objects.get(email=payload['email'])
        serializer = ListEmployeeSerializer(employee)

        response = self.client.get(EMPLOYEES_LIST)
        self.assertIn(serializer.data, response.data)
