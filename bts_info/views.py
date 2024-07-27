from django.contrib import messages
from django.shortcuts import render
from django.views import View

from bts_info.forms import SiteInfoForm
from bts_info.services.main import get_site_data
from services.mixins import LoginMixin


class BtsInfo(LoginMixin, View):
    """View for handling BTS information."""

    template_name = 'bts_info/bts_info.html'

    def get(self, request, *args, **kwargs):
        """Handle GET requests to render a form for inputting BTS information."""
        form = SiteInfoForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """Handle POST requests to process the form submission and display."""
        bts_form = SiteInfoForm(request.POST)
        if bts_form.is_valid():
            bts_id = bts_form.cleaned_data['bts_id']
            source = bts_form.cleaned_data['source']

            try:
                sites, polygons, lat, lon = get_site_data(bts_id, source)
            except RuntimeError:
                messages.error(request, f'Site with id {bts_id} was not found')
                return render(request, self.template_name, {'form': bts_form})

            context = {
                'form': bts_form,
                'source': source,
                'latitude': lat,
                'longitude': lon,
            }

            if sites:
                context['headers'] = sites[0].keys()
                context['sites'] = sites
            else:
                messages.error(request, f'Site with id {bts_id} was not found')

            if polygons:
                context['sector_polygons'] = polygons

            return render(request, 'bts_info/bts_info.html', context)
