from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from users.forms import UserRegistrationForm
from users.ldap_authentication import get_unit_ldap, is_ldap_bind


class UserRegistration(CreateView):
    """View for handling user registration."""

    model = User
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    success_message = 'User registration was successful'
    error_kcell_message = 'You used not Kcell account. Please, use your Kcell account'

    def form_valid(self, form):
        """Handle the case when the registration form is valid."""
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        if is_ldap_bind(email, password):
            response = super().form_valid(form)
            self.add_user_to_groups(self.object, email, password)
            messages.success(self.request, self.success_message)
            return response

        form.add_error(
            None,
            self.error_kcell_message,
        )
        return self.form_invalid(form)

    def add_user_to_groups(self, user, email, passwd):
        """Add users to groups."""
        group_name = 'Regular Users'
        try:
            regular_users_group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            regular_users_group = Group.objects.create(name=group_name)
        user.groups.add(regular_users_group)

        rnpo_units = [
            'Сектор стратегического планирования радиосети',
            'Сектор планирования сети',
            'Сектор оптимизации радиосети',
        ]
        rnpo_group = 'RNPO Users'
        unit = get_unit_ldap(email, passwd)
        if unit in rnpo_units:
            try:
                special_group = Group.objects.get(name=rnpo_group)
            except Group.DoesNotExist:
                special_group = Group.objects.create(name=rnpo_group)
            user.groups.add(special_group)


class UserLogin(LoginView):
    """View for handling user login."""

    template_name = 'users/login.html'
    success_url = reverse_lazy('index')
    success_message = 'You are logged in'

    def form_valid(self, form):
        """Handle the case when the login form is valid."""
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle the case when the login form is invalid."""
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return super().form_invalid(form)

        if is_ldap_bind(user.email, password):
            user.set_password(password)
            user.save()
            authenticated_user = authenticate(
                self.request,
                username=username,
                password=password,
            )
            login(self.request, authenticated_user)
            messages.success(self.request, self.success_message)
            return redirect(self.success_url)
        return super().form_invalid(form)


class UserLogout(LogoutView):
    """View for handling user logout."""

    next_page = reverse_lazy('index')
    success_message = 'You are logged out'

    def dispatch(self, request, *args, **kwargs):
        """Handle the HTTP request for user logout."""
        if request.user.is_authenticated:
            messages.success(self.request, self.success_message)
        return super().dispatch(request, *args, **kwargs)
