from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from point_in_region import get_regions

from bts_files.services.main import get_file_content
from services.mixins import GroupRequiredMixin, LoginMixin

FILE_TYPES = ('kml', 'nbf', 'excel')
TECHNOLOGIES = ('GSM', 'WCDMA', 'LTE', 'NR')


class BtsFiles(LoginMixin, GroupRequiredMixin, View):
    """A view for handling BTS files."""

    required_groups = ['RNPO Users', 'BTS Files']

    def get(self, request, *args, **kwargs):
        """Render form to select needed parameters for BTS file."""
        return render(request, 'bts_files/bts_files.html', {
            'file_types': FILE_TYPES,
            'technologies': TECHNOLOGIES,
            'regions': get_regions(is_sorted=True),
        })

    def post(self, request, *args, **kwargs):
        """Create a BTS file in requested format, technologies and regions."""
        file_type = request.POST.get('file-type')
        technologies = request.POST.getlist('technologies')
        regions = request.POST.getlist('regions')

        file_content = get_file_content(file_type, technologies, regions)

        if file_type == 'excel':
            content_type = 'application/vnd.ms-excel'
            file_name = 'bts_file.xlsx'
        else:
            content_type = 'text/plain'
            file_name = f'bts_file.{file_type}'

        response = HttpResponse(file_content, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'

        return response


class KmlOnly(LoginMixin, GroupRequiredMixin, View):
    """A view for handling KML files."""

    required_groups = ['Partial Access Users']

    def get(self, request, *args, **kwargs):
        """Render form to select needed parameters for KML file."""
        return render(request, 'bts_files/kml.html', {
            'technologies': TECHNOLOGIES,
            'regions': get_regions(is_sorted=True),
        })

    def post(self, request, *args, **kwargs):
        """Create a KML file with BTS data based on selected technologies and regions."""
        file_type = 'kml'
        technologies = request.POST.getlist('technologies')
        regions = request.POST.getlist('regions')

        file_content = get_file_content(file_type, technologies, regions)

        response = HttpResponse(file_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="bts_file.kml"'

        return response
