from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class LoginMixin(LoginRequiredMixin):
    """Mixin for views that require login."""

    login_url = reverse_lazy('login')

    def handle_no_permission(self):
        """Handle the case when the user does not signed in."""
        messages.error(
            self.request,
            'You are not signed in! Please, sign in',
        )
        return super().handle_no_permission()


class GroupMixin(AccessMixin):
    """Mixin for views that require group-based permissions."""

    allowed_groups = [settings.POU_GROUP]

    def handle_no_permission(self):
        """Handle when the user does not have permission."""
        if self.request.user.is_authenticated:
            messages.error(
                self.request,
                'You do not have permission to access this page',
            )
        else:
            messages.error(
                self.request,
                'You are not signed in! Please sign in',
            )
        return redirect(self.request.META.get('HTTP_REFERER', '/'))

    def dispatch(self, request, *args, **kwargs):
        """Check authentication and required permissions, then proceeds to dispatching process."""
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        user_groups = request.user.groups.values_list('name', flat=True)
        if self.allowed_groups and not any(group in user_groups for group in self.allowed_groups):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
