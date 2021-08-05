from enum import auto
import leavemanagementsys
from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from users.models import CustomUser


class LeaveRequest(models.Model):
    applied_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    from_date = models.DateField(default=timezone.now)
    to_date = models.DateField(default=timezone.now)
    leave_type = models.CharField(max_length=10, default='Personal',)
    number_of_days = models.IntegerField()
    status = models.CharField(max_length=10, default='Pending',)
    remark = models.CharField(max_length=50, default='NIL')

    def __str__(self):
        return f'description:{self.description}'
