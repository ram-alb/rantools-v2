from django.contrib import messages
from django.shortcuts import render
from django.views.generic.edit import FormView

from bts_info.forms import SiteInfoForm
from bts_info.services.main import get_site_data
from services.mixins import LoginMixin


class BtsInfo(LoginMixin, FormView):
    """View for handling BTS information."""

    template_name = 'bts_info/bts_info.html'
    form_class = SiteInfoForm

    def form_valid(self, form):
        """Handle valid form."""
        bts_id = form.cleaned_data['bts_id']
        source = form.cleaned_data['source']

        try:
            sites, polygons, lat, lon = get_site_data(bts_id, source)
        except RuntimeError:
            messages.error(self.request, f'Site with id {bts_id} was not found')
            return self.form_invalid(form)

        context = self.get_context_data(form=form, source=source, latitude=lat, longitude=lon)

        context['headers'] = sites[0].keys()
        context['sites'] = sites

        if polygons:
            context['sector_polygons'] = polygons

        return render(self.request, self.template_name, context)
