from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from bts_files.services.main import get_file_content
from services.mixins import GroupRequiredMixin, LoginMixin

FILE_TYPES = ('kml', 'nbf', 'excel')
TECHNOLOGIES = ('GSM', 'WCDMA', 'LTE', 'NR')
REGIONS = (
    'Astana-region',
    'Aktobe-region',
    'Almaty-region',
    'Atyrau-region',
    'Karaganda-region',
    'Kostanay-region',
    'Kyzylorda-region',
    'Mangystau-region',
    'Pavlodar-region',
    'North-Kazakhstan',
    'South-Kazakhstan',
    'East-Kazakhstan',
    'Zhambyl-region',
    'West-Kazakhstan',
    'Kazmin',
)


class BtsFiles(LoginMixin, GroupRequiredMixin, View):
    """A view for handling BTS files."""

    required_group = 'RNPO Users'

    def get(self, request, *args, **kwargs):
        """Render form to select needed parameters for BTS file."""
        return render(request, 'bts_files/bts_files.html', {
            'file_types': FILE_TYPES,
            'technologies': TECHNOLOGIES,
            'regions': sorted(REGIONS),
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
