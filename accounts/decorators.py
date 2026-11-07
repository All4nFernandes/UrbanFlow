from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def role_required(*allowed_roles):
    if not allowed_roles:
        raise ValueError("role_required exige pelo menos um papel permitido.")

    allowed_values = frozenset(
        str(getattr(role, "value", role)) for role in allowed_roles
    )

    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            user_role = getattr(request.user, "role", None)
            user_role = str(getattr(user_role, "value", user_role))

            if user_role not in allowed_values:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator