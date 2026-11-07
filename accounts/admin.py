from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from .admin_permissions import UrbanFlowAdminAccessMixin


@admin.register(User)
class UrbanFlowUserAdmin(UrbanFlowAdminAccessMixin, UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("UrbanFlow", {"fields": ("role", "cpf")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("UrbanFlow", {"fields": ("role", "cpf")}),
    )
    list_display = ("username", "first_name", "last_name", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "first_name", "last_name", "email", "cpf")