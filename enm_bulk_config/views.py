from django.shortcuts import render
from django.views import View


class EnmBulkConfigView(View):
    """View for handling ENM bulk configuration."""

    template_name = "enm_bulk_config/index.html"

    def get(self, request, *args, **kwargs):
        """Handle GET requests for the ENM bulk configuration page."""
        return render(request, self.template_name)
