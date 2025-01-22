from datetime import date, timedelta

from django.contrib import messages
from django.shortcuts import render
from django.views import View

from services.mixins import LoginMixin
from sites_count.forms import SiteCountForm
from sites_count.services.main import get_site_data


class SitesCountView(LoginMixin, View):
    """A view for displaying site counts."""

    template_path = 'sites_count/index.html'

    year = 2023
    month = 5
    day = 15
    started_date = date(year, month, day)

    def get(self, request, *args, **kwargs):
        """Handle GET requests to the view and render the site count form."""
        chosen_date = date.today()
        sites_data, chosen_date = self.get_sites_data('operator', chosen_date, request)

        form = SiteCountForm()
        form.fields['date'].initial = chosen_date
        context = {
            'form': form,
            'sites': sites_data,
            'header': 'Operator',
        }
        return render(request, self.template_path, context)

    def post(self, request, *args, **kwargs):
        """Handle POST requests to the view and process the submitted form."""
        form = SiteCountForm(request.POST)
        if form.is_valid():
            requested_date = form.cleaned_data['date']
            validation_message = self.validate_date(requested_date)

            if validation_message:
                form.add_error('date', validation_message)
                return render(request, self.template_path, {'form': form})

            table_type = form.cleaned_data['table_type']
            sites_data, _ = self.get_sites_data(table_type, requested_date, request)

            header = table_type.capitalize()
            context = {'form': form, 'sites': sites_data, 'header': header}

            return render(request, self.template_path, context)

        return render(request, self.template_path, {'form': form})

    def get_sites_data(self, table_type, chosen_date, request):
        """Return site data for a given date."""
        sites_data = get_site_data(table_type, chosen_date)
        if not sites_data:
            yesterday = date.today() - timedelta(days=1)
            sites_data = get_site_data(table_type, yesterday)
            messages.error(
                request,
                f'No data for {chosen_date}. Data for {yesterday} is shown.',
            )
            return sites_data, yesterday
        return sites_data, chosen_date

    def validate_date(self, requested_date):
        """Validate the requested date."""
        if requested_date < self.started_date:
            return 'No data before 15 May 2023'
        elif requested_date > date.today():
            return 'No data from the future :)'
        return None
