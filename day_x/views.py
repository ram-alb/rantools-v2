from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from config.redis import is_locked
from day_x.tasks import DAYX_FILE_LOCK_KEY, update_dayx_file
from services.mixins import GroupRequiredMixin, LoginMixin


class DayXIndexView(LoginMixin, GroupRequiredMixin, TemplateView):
    """View for displaying the main page of the DayX section."""

    template_name = 'day_x/index.html'
    required_groups = ['DayX']


class UpdateDayXFileView(LoginMixin, GroupRequiredMixin, RedirectView):
    """View for triggering the update process of the DayX file."""

    required_groups = ['DayX']
    pattern_name = 'dayX'

    def get(self, request, *args, **kwargs):
        """Handle GET requests to trigger or check the status of the DayX file update task."""
        if is_locked(DAYX_FILE_LOCK_KEY):
            messages.error(
                request,
                'DayX file updating is in progress. It will be sent to your email. Please wait.',
            )
        else:
            update_dayx_file.delay()
            messages.success(request, 'DayX file will be sent to your email shortly. Please wait.')
        return super().get(request, *args, **kwargs)
