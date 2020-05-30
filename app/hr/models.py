from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin


POSITIONS = [
    ('director', 'Director'),
    ('manager', 'Manager'),
    ('officer', 'Officer'),
]


class UserManager(BaseUserManager):

    def create_user(self, email, password, position, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Employees must have an email address')
        if not position:
            raise ValueError('Missing employee position')
        if position == 'director':
            base_salary = 5000.00
        elif position == 'manager':
            base_salary = 3000.00
        elif position == 'officer':
            base_salary = 2000.00
        else:
            raise ValueError('Unknown position')

        user = self.model(
            email=self.normalize_email(email),
            base_salary=base_salary,
            **extra_fields
        )
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Creates and saves a superuser"""
        user = self.create_user(email,password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=40, choices=POSITIONS)
    joined_on = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    base_salary = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    attendance = models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'{self.position}, {self.name}'

    def net_salary(self):
        return self.base_salary / 20 * self.attendance
