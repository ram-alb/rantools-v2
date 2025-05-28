from django.views import View
from django.shortcuts import render


class EnmBulkConfigView(View):
    """View for handling ENM bulk configuration."""

    template_name = 'enm_bulk_config/index.html'

    def get(self, request, *args, **kwargs):
        # Handle GET request
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Handle POST request
        pass
