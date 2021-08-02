from enum import auto
import leavemanagementsys
from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from users.models import CustomUser


class LeaveRequest(models.Model):
    # TYPE_OF_LEAVE_CHOICES = [
    #     ('P', 'Personal'),
    #     ('L', 'LOP_Leave'),
    #     ('C', 'Covid_Support'),
    # ]
    # LEAVE_STATUS_CHOICES = [
    #     ('A', 'Approve'),
    #     ('R', 'Reject'),
    #     ('P', 'Pending'),
    #     ('C', 'Cancel'),
    # ]
    applied_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    from_date = models.DateField(unique=True, default=timezone.now)
    to_date = models.DateField(unique=True, default=timezone.now)
    leave_type = models.CharField(max_length=10, default='Personal',)
    number_of_days = models.IntegerField()
    status = models.CharField(max_length=10, default='Pending',)
    remark = models.CharField(max_length=50, default='NIL')

    # USERNAME_FIELD = 'applied_user'

    def __str__(self):
        return f'description:{self.description}'
