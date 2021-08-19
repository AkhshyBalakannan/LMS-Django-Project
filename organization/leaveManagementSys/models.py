from django.db import models
from django.utils import timezone
from users.models import CustomUser

LEAVE_TYPE = (
    ('personal', 'personal'),
    ('lop', 'lop'),
    ('sick-covid', 'sick-covid'),
)


class LeaveRequest(models.Model):
    applied_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    from_date = models.DateField(default=timezone.now)
    to_date = models.DateField(default=timezone.now)
    leave_type = models.CharField(
        max_length=20, choices=LEAVE_TYPE, default='personal',)
    number_of_days = models.IntegerField(blank=True)
    status = models.CharField(max_length=10, default='Pending',)
    remark = models.CharField(max_length=50, default='NIL')

    def save(self, *args, **kwargs):
        self.number_of_days = (self.to_date - self.from_date).days + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f'description:{self.description}'


class LeaveDates(models.Model):
    applied_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    dates = models.DateField()

    def __str__(self):
        return f'{self.dates}'
