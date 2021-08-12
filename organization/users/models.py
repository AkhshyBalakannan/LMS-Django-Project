from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField


class CustomUser(AbstractUser):
    profile_pic = models.ImageField(
        default='default.jpg', upload_to='profile_pic')
    address = models.CharField(
        max_length=200, default='Bay Area, San Francisco, CA')
    is_admin_employee = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=10, default=9999999999)
    leave_eligible = models.IntegerField(default=12)
    leave_taken = models.IntegerField(default=0)
    leave_remaining = models.IntegerField(default=12)
    lop_leave_taken = models.IntegerField(default=0)
    covid_leave_taken = models.IntegerField(default=0)

    def __str__(self):
        return self.username
