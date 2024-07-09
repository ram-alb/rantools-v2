from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from users.forms import UserRegistrationForm
from users.ldap_authentication import is_ldap_bind, is_member_pou


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
            user = form.save(commit=False)
            user.save()
            self.assign_groups(user, email)
            messages.success(self.request, self.success_message)
            return super().form_valid(form)

        form.add_error(
            None,
            self.error_kcell_message,
        )
        return self.form_invalid(form)

    def assign_groups(self, user, email):
        """Assign user to appropriate groups based on LDAP membership."""
        is_pou = is_member_pou(email)
        group_regular, _ = Group.objects.get_or_create(name='Regular Users')
        user.groups.add(group_regular)

        if is_pou:
            group_pou, _ = Group.objects.get_or_create(name='POU Users')
            user.groups.add(group_pou)


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
