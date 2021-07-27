from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User


class LeaveRequest(models.Model):
    applied_user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    applied_date = models.DateTimeField(default=timezone.now)
    eligible_leave = models.IntegerField(default=2)
    status = models.BooleanField(default=0)
    approved_leave = models.IntegerField(default=0)
    rejected_leave = models.IntegerField(default=0)

    def __str__(self):
        return f'User Applied: {self.applied_user} - Reason: {self.reason}'
