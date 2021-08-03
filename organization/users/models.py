from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_employee = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)
    leave_eligible = models.IntegerField(default=12)
    leave_taken = models.IntegerField(default=0)
    leave_remaining = models.IntegerField(default=12)
    lop_leave_taken = models.IntegerField(default=0)
    covid_leave_taken = models.IntegerField(default=0)

    def __str__(self):
        return self.username
