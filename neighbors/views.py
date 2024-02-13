import os

from django.contrib import messages
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from neighbors.forms import UploadNeighborsForm
from neighbors.services.excel import is_excel_file
from neighbors.services.gsm.g2u import generate_g2u_nbr_adding_import_report
from neighbors.services.wcdma.u2g import generate_u2g_nbr_adding_import_report
from services.mixins import LoginMixin


class Index(LoginMixin, TemplateView):
    """Render the index page of the neighbors app."""

    template_name = 'neighbors/index.html'


class GsmToUmtsNbr(LoginMixin, View):
    """A view for managing G2U neighbors."""

    def get(self, request, direction, *args, **kwargs):
        """Handle GET request."""
        upload_nbr_form = UploadNeighborsForm()
        return render(
            request,
            'neighbors/gu.html',
            {'form': upload_nbr_form, 'direction': direction},
        )

    def post(self, request, direction, *args, **kwargs):
        """Handle POST request."""
        nbr_form = UploadNeighborsForm(request.POST, request.FILES)
        if nbr_form.is_valid():
            nbr_excel = request.FILES['neighbors_excel']

            if not is_excel_file(nbr_excel.name):
                messages.error(request, 'Uploaded file is not excel file')
                return redirect(reverse_lazy('nbr-g2u'))

            if direction == 'G2U':
                report_path = generate_g2u_nbr_adding_import_report(nbr_excel)
            elif direction == 'U2G':
                report_path = generate_u2g_nbr_adding_import_report(nbr_excel)

            with open(report_path, 'rb') as report:
                response = HttpResponse(report.read(), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename="{direction}-nbr.zip"'

            os.remove(report_path)
            return response

        messages.error(request, 'Submited form is invalid')
        return redirect(reverse_lazy('nbr-gu'))


class DownloadGUTemplate(LoginMixin, View):
    """A view for downloading neighbor template for planned neighbors."""

    def get(self, request, direction):
        """Handle a GET request."""
        template_path = 'neighbors/reports/templates/gu.xlsx'

        with open(template_path, 'rb') as template:
            response = HttpResponse(template.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{direction}.xlsx"'

        return response
