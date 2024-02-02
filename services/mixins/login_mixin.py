from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
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
