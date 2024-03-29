from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from {{cookiecutter.project_name}}.accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ["email", "password"]}),
        ("Permissions", {"fields": ["is_active", "is_staff", "is_superuser"]}),
        ("Important dates", {"fields": ["last_login", "date_joined"]}),
    )
    add_fieldsets = (
        (None, {"classes": ["wide"], "fields": ["email", "password1", "password2"]}),
    )
    search_fields = ("email",)
    ordering = ("email",)
    list_display = ("email", "is_staff")
