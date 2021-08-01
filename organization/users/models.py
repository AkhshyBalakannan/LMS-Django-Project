from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    leave_eligible = models.IntegerField(default=0)
    leave_taken = models.IntegerField(default=0)
    leave_remaining = models.IntegerField(default=0)
    lop_leave_taken = models.IntegerField(default=0)
    covid_leave_taken = models.IntegerField(default=0)
