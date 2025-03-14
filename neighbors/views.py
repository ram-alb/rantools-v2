import os

from django.contrib import messages
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from neighbors.forms import UploadNeighborsForm
from neighbors.services.gsm import g2g, g2l, g2u
from neighbors.services.wcdma import u2g, u2l, u2u
from services.mixins import GroupRequiredMixin, LoginMixin


class Index(LoginMixin, GroupRequiredMixin, TemplateView):
    """Render the index page of the neighbors app."""

    template_name = 'neighbors/index.html'
    required_groups = ['RNPO Users']


class NbrImport(LoginMixin, GroupRequiredMixin, View):
    """A view for managing neighbors."""

    required_groups = ['RNPO Users']

    def get(self, request, direction, *args, **kwargs):
        """Handle GET request."""
        upload_nbr_form = UploadNeighborsForm()
        return render(
            request,
            'neighbors/import.html',
            {'form': upload_nbr_form, 'direction': direction},
        )

    def post(self, request, direction, *args, **kwargs):
        """Handle POST request."""
        genereate_import_report_funcs = {
            'G2G': g2g.generate_g2g_nbr_adding_import_report,
            'G2U': g2u.generate_g2u_nbr_adding_import_report,
            'G2L': g2l.generate_g2l_nbr_adding_import_report,
            'U2G': u2g.generate_u2g_nbr_adding_import_report,
            'U2U': u2u.generate_u2u_nbr_adding_import_report,
            'U2L': u2l.generate_u2l_nbr_adding_import_report,
        }
        nbr_form = UploadNeighborsForm(request.POST, request.FILES)

        if nbr_form.is_valid():
            enm = nbr_form.cleaned_data['enm']
            nbr_excel = request.FILES['neighbors_excel']
            report_path = genereate_import_report_funcs[direction](nbr_excel, enm)

            with open(report_path, 'rb') as report:
                response = HttpResponse(report.read(), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename="{direction}-nbr.zip"'

            os.remove(report_path)
            return response

        messages.error(request, 'Submited form is invalid')
        return redirect(reverse_lazy('nbr-import', kwargs={'direction': direction}))


class DownloadTemplate(LoginMixin, GroupRequiredMixin, View):
    """A view for downloading neighbor template for planned neighbors."""

    required_groups = ['RNPO Users']

    def get(self, request, direction):
        """Handle a GET request."""
        if '2L' in direction:
            template_path = 'neighbors/reports/templates/ToLTE.xlsx'
        else:
            template_path = 'neighbors/reports/templates/GU.xlsx'

        with open(template_path, 'rb') as template:
            response = HttpResponse(template.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{direction}.xlsx"'

        return response
