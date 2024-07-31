from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import reverse_lazy


class LoginMixin(LoginRequiredMixin):
    """Mixin for views that require login."""

    login_url = reverse_lazy('login')
    required_group = None
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

        if self.required_group is not None:
            if not self.request.user.groups.filter(name=self.required_group).exists():
                messages.error(
                    self.request,
                    self.no_permission_msg,
                )
                return redirect(self.redirect_url)

        return super().handle_no_permission()


class GroupRequiredMixin(UserPassesTestMixin):
    """Mixin to check if the user belongs to a specific group."""

    required_group = None

    def test_func(self) -> bool:
        """Check if the current user belongs to the specified group."""
        if self.required_group:
            try:
                group = Group.objects.get(name=self.required_group)
            except Group.DoesNotExist:
                return False
            return self.request.user.groups.filter(name=group.name).exists()

        return False
