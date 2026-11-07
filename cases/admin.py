from django.contrib import admin

from accounts.admin_permissions import UrbanFlowAdminAccessMixin
from .models import Case


@admin.register(Case)
class CaseAdmin(UrbanFlowAdminAccessMixin, admin.ModelAdmin):
    list_display = ("id", "title", "category", "status", "requester", "created_at")
    list_filter = ("status", "category", "is_public", "created_at")
    search_fields = ("title", "description", "requester__username")
    readonly_fields = ("created_at", "updated_at")