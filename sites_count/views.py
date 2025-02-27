from datetime import date, timedelta

from django.contrib import messages
from django.shortcuts import render
from django.views import View

from services.mixins import LoginMixin
from sites_count.forms import SiteCountForm
from sites_count.services.fetcher import fetch_site_counts

START_DAY = 15
START_MONTH = 5
START_YEAR = 2023
OPERATOR_REGION_START_DAY = 1
OPERATOR_REGION_START_MONTH = 2
OPERATOR_REGION_START_YEAR = 2025


class SitesCountView(LoginMixin, View):
    """A view to display site count data."""

    started_date = date(START_YEAR, START_MONTH, START_DAY)
    operator_region_start_date = date(
        OPERATOR_REGION_START_YEAR,
        OPERATOR_REGION_START_MONTH,
        OPERATOR_REGION_START_DAY,
    )

    template_name = 'sites_count/index.html'

    def get(self, request):
        """Display the form to request site count data."""
        requested_date = date.today()
        default_group_by = 'operator'

        sites_data, used_date = self.get_sites_data(default_group_by, requested_date, request)
        form = SiteCountForm(initial={'date': used_date, 'group_by': default_group_by})

        return render(
            request,
            self.template_name,
            {'form': form, 'data': sites_data, 'group_by': default_group_by},
        )

    def post(self, request):
        """Display the site count data for the requested date."""
        form = SiteCountForm(request.POST)
        if form.is_valid():
            requested_date = form.cleaned_data['date']
            group_by = form.cleaned_data['group_by']

            validation_message = self.validate_date(requested_date, group_by)
            if validation_message:
                form.add_error('date', validation_message)
                return render(request, self.template_name, {'form': form})

            sites_data, final_date = self.get_sites_data(group_by, requested_date, request)
            form = SiteCountForm(initial={'date': final_date, 'group_by': group_by})

            return render(
                request,
                self.template_name,
                {'form': form, 'data': sites_data, 'group_by': group_by},
            )

    def validate_date(self, requested_date, group_by):
        """Validate the requested date."""
        if requested_date < self.started_date:
            formated_date = self.started_date.strftime('%d %B %Y')
            return f'No data before {formated_date}'

        if requested_date > date.today():
            return 'No data from the future :)'

        if group_by not in {'operator', 'vendor', 'region'}:
            if requested_date < self.operator_region_start_date:
                formated_date = self.operator_region_start_date.strftime('%d %B %Y')
                return f'No data before {formated_date}'
        return None

    def get_sites_data(self, group_by, requested_date, request):
        """Return site data for a given date."""
        sites_data = fetch_site_counts(group_by, requested_date)

        if sites_data:
            return sites_data, requested_date

        yesterday = date.today() - timedelta(days=1)
        sites_data = fetch_site_counts(group_by, yesterday)
        if sites_data:
            formated_requested_date = requested_date.strftime('%d %B %Y')
            formated_yesterday = yesterday.strftime('%d %B %Y')
            error_message = (
                f'Data for {formated_requested_date} is not available yet. '
                f'Displaying data for {formated_yesterday}.'
            )
            messages.error(
                request,
                error_message,
            )
            return sites_data, yesterday

        formated_date = requested_date.strftime('%d %B %Y')
        messages.error(request, f'No data for {formated_date}.')

        return {}, requested_date
