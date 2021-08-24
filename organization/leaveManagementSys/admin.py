'''Django Admin Page Setup'''
from django.contrib import admin
from leavemanagementsys.models import LeaveDates, LeaveRequest

admin.site.register(LeaveRequest)
admin.site.register(LeaveDates)
