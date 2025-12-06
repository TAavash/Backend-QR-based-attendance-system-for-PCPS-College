from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Fields to show in the admin list view
    list_display = ('username', 'email', 'role', 'uid', 'is_staff')

    # Add custom fields to Django admin's edit form
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('uid', 'role')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('uid', 'role')}),
    )
