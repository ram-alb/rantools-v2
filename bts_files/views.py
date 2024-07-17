from django.shortcuts import render
from django.views import View

FILE_TYPES = ('kml', 'nbf', 'excel')
TECHNOLOGIES = ('NR', 'LTE', 'WCDMA', 'GSM')
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


class BtsFiles(View):
    """A view for handling BTS files."""

    def get(self, request, *args, **kwargs):
        """Render form to select needed parameters for BTS file."""
        return render(request, 'bts_files/bts_files.html', {
            'file_types': FILE_TYPES,
            'technologies': TECHNOLOGIES,
            'regions': sorted(REGIONS),
        })
