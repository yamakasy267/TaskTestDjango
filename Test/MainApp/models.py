from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import datetime
from Test import settings

class Roles(models.Model):
    role_id = models.BigAutoField(primary_key=True)
    role_name = models.CharField(max_length=1000)

    def __str__(self):
        return self.role_name


class UserStatus(models.Model):
    status_id = models.BigAutoField(primary_key=True)
    status_name = models.CharField(max_length=1000)

    def __str__(self):
        return self.status_name


class CustomUser(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=1000, null=True, blank=True)
    surname = models.CharField(max_length=1000, null=True, blank=True)
    email = models.EmailField(max_length=1000, db_index=True)
    password = models.CharField(max_length=1000, blank=True, null=True)
    role = models.ForeignKey(Roles, on_delete=models.PROTECT)
    user_status = models.ForeignKey(UserStatus, on_delete=models.PROTECT)
    last_login = models.DateTimeField(blank=True, null=True)
    user_registration_date = models.DateTimeField()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'{self.name} {self.surname}'


class UsersFiles(models.Model):
    id = models.BigAutoField(primary_key=True)
    file_name = models.CharField(max_length=1000)
    file = models.FileField()
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.user.__str__()} {self.file_name}"
