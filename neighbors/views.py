import os

from django.contrib import messages
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from neighbors.forms import UploadNeighborsForm
from neighbors.services.excel import is_excel_file
from neighbors.services.gsm.g2u import generate_g2u_nbr_addition_report
from services.mixins import LoginMixin


class Index(LoginMixin, TemplateView):
    """Render the index page of the neighbors app."""

    template_name = 'neighbors/index.html'


class GsmToUmtsNbr(LoginMixin, View):
    """A view for managing G2U neighbors."""

    def get(self, request, *args, **kwargs):
        """Handle GET request."""
        upload_g2u_nbr_form = UploadNeighborsForm()
        return render(request, 'neighbors/g2u.html', {'form': upload_g2u_nbr_form})

    def post(self, request, *args, **kwargs):
        """Handle POST request."""
        g2u_nbr_form = UploadNeighborsForm(request.POST, request.FILES)
        if g2u_nbr_form.is_valid():
            g2u_nbr_excel = request.FILES['neighbors_excel']

            if not is_excel_file(g2u_nbr_excel.name):
                messages.error(request, 'Uploaded file is not excel file')
                return redirect(reverse_lazy('nbr-g2u'))

            report_path = generate_g2u_nbr_addition_report(g2u_nbr_excel)
            with open(report_path, 'rb') as report:
                response = HttpResponse(report.read(), content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename="G2U-nbr.zip"'

            os.remove(report_path)
            return response

        messages.error(request, 'Submited form is invalid')
        return redirect(reverse_lazy('nbr-g2u'))
