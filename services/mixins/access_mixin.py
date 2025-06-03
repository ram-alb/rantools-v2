from functools import wraps
from typing import List, Optional

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

# URLs
LOGIN_URL = reverse_lazy("login")
INDEX_URL = reverse_lazy("index")

# Authentication messages
NOT_SIGNED_IN_MSG = "You are not signed in! Please, sign in"
NO_PERMISSION_MSG = "You do not have permission to access this page."


def login_required_mixin(required_groups: Optional[List[str]] = None):
    """
    Provide LoginMixin functionality for function-based views.

    Checks if user is authenticated and optionally belongs to required groups.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, NOT_SIGNED_IN_MSG)
                return redirect(f"{LOGIN_URL}?next={request.path}")

            if required_groups is not None:
                if not request.user.groups.filter(name__in=required_groups).exists():
                    messages.error(request, NO_PERMISSION_MSG)
                    return redirect(INDEX_URL)

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


class LoginMixin(LoginRequiredMixin):
    """Mixin for views that require login."""

    login_url = LOGIN_URL
    redirect_url = INDEX_URL
    required_groups = None
    not_signed_in_msg = NOT_SIGNED_IN_MSG
    no_permission_msg = NO_PERMISSION_MSG

    def handle_no_permission(self):
        """Handle the case when the user does not signed in."""
        if not self.request.user.is_authenticated:
            messages.error(self.request, NOT_SIGNED_IN_MSG)
            return super().handle_no_permission()

        if self.required_groups is not None:
            if not self._is_user_belongs_to_required_groups():
                messages.error(self.request, NO_PERMISSION_MSG)
                return redirect(self.redirect_url)

        return super().handle_no_permission()

    def _is_user_belongs_to_required_groups(self) -> bool:
        """Check if user belongs to any of the required groups."""
        return self.request.user.groups.filter(name__in=self.required_groups).exists()


class GroupRequiredMixin(UserPassesTestMixin):
    """Mixin to check if the user belongs to at least one group from the required list."""

    required_groups = []

    def test_func(self) -> bool:
        """Check if the current user belongs to at least one of the specified groups."""
        if self.required_groups:
            user_groups = set(self.request.user.groups.values_list("name", flat=True))
            return bool(user_groups.intersection(self.required_groups))

        return False
