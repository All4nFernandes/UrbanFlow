class UrbanFlowAdminAccessMixin:
    def _can_manage_admin_data(self, request):
        return (
            request.user.is_authenticated
            and request.user.is_active
            and getattr(request.user, "role", None) == "superuser"
        )

    def has_module_permission(self, request):
        return self._can_manage_admin_data(request)

    def has_view_permission(self, request, obj=None):
        return self._can_manage_admin_data(request)

    def has_add_permission(self, request):
        return self._can_manage_admin_data(request)

    def has_change_permission(self, request, obj=None):
        return self._can_manage_admin_data(request)

    def has_delete_permission(self, request, obj=None):
        return self._can_manage_admin_data(request)