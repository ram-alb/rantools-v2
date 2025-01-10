from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from services.mixins import GroupRequiredMixin, LoginMixin
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse_lazy
from time import sleep


class DayX(LoginMixin, GroupRequiredMixin, TemplateView):
    template_name = 'day_x/index.html'
    required_group = 'DayX'


class LongView(LoginMixin, GroupRequiredMixin, View):
    required_group = 'DayX'
    def get(self, request, *args, **kwargs):
        sleep(10)
        messages.success(request, 'File updated')
        return redirect(reverse_lazy('dayX'))