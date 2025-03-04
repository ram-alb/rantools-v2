from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from users.forms import UserRegistrationForm
from users.ldap_authentication import get_groups_ldap, is_ldap_bind


class UserRegistration(CreateView):
    """View for handling user registration."""

    model = User
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    success_message = 'User registration was successful'
    error_kcell_message = 'You used not Kcell account. Please, use your Kcell account'
    error_email_exists_message = 'A user with this email already exists.'

    def form_valid(self, form):
        """Handle the case when the registration form is valid."""
        email = form.cleaned_data['email'].lower()

        form.instance.email = email
        form.instance.username = form.cleaned_data['username'].lower()

        password = form.cleaned_data['password1']

        if User.objects.filter(email=email).exists():
            form.add_error('email', self.error_email_exists_message)
            return self.form_invalid(form)

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

        ldap_groups = get_groups_ldap(email, passwd)
        if ldap_groups is None:
            return

        rnpo_group = 'RNPO Users'
        if 'CN=NDS-RNPOU' in ', '.join(ldap_groups):
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
        username = form.cleaned_data['username'].lower()
        if '@' in username:
            username = username.split('@')[0]
        password = form.cleaned_data['password']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(self.request, f"User '{username}' does not exist. Please register first")
            return redirect(
                reverse_lazy('registration'),
            )

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
