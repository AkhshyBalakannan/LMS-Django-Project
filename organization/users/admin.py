from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'is_employee', 'is_manager', 'leave_eligible',
        'leave_taken', 'leave_remaining', 'lop_leave_taken',
        'covid_leave_taken',
    )

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('is_employee', 'is_manager', 'leave_eligible',
                       'leave_taken', 'leave_remaining', 'lop_leave_taken',
                       'covid_leave_taken',)
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('is_employee', 'is_manager', 'leave_eligible',
                       'leave_taken', 'leave_remaining', 'lop_leave_taken',
                       'covid_leave_taken',)
        })
    )


admin.site.register(CustomUser, CustomUserAdmin)
