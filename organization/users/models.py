from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    '''Custom User with partial field of user class'''
    is_manager = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=10, default=1234567890)
    profile_pic = models.ImageField(
        upload_to='profile_pic/', default='default.jpg')
    address = models.CharField(
        max_length=200, default='Bay Area, San Francisco, CA')
    report_to = models.CharField(max_length=150, default='admin')
    leave_eligible = models.IntegerField(default=6)
    leave_remaining = models.IntegerField(default=6)

    def __str__(self):
        return self.username
