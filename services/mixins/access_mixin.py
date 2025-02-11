from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class LoginMixin(LoginRequiredMixin):
    """Mixin for views that require login."""

    login_url = reverse_lazy('login')
    required_groups = None
    redirect_url = reverse_lazy('index')
    not_signed_in_msg = 'You are not signed in! Please, sign in'
    no_permission_msg = 'You do not have permission to access this page.'

    def handle_no_permission(self):
        """Handle the case when the user does not signed in."""
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                self.not_signed_in_msg,
            )
            return super().handle_no_permission()

        if self.required_groups is not None:
            if not self.request.user.groups.filter(name__in=self.required_groups).exists():
                messages.error(
                    self.request,
                    self.no_permission_msg,
                )
                return redirect(self.redirect_url)

        return super().handle_no_permission()


class GroupRequiredMixin(UserPassesTestMixin):
    """Mixin to check if the user belongs to at least one group from the required list."""

    required_groups = []

    def test_func(self) -> bool:
        """Check if the current user belongs to at least one of the specified groups."""
        if self.required_groups:
            user_groups = set(self.request.user.groups.values_list("name", flat=True))
            return bool(user_groups.intersection(self.required_groups))

        return False
