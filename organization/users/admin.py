'''Django Admin Page Setup'''
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # pylint: disable=relative-beyond-top-level


class CustomUserAdmin(UserAdmin):
    '''Display in Admin Page'''
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'is_manager', 'phone_number', 'leave_eligible', 'leave_remaining',)

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'profile_pic', 'phone_number')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('is_manager', 'report_to', 'leave_eligible', 'leave_remaining',)
        })
    )


admin.site.register(CustomUser, CustomUserAdmin)
