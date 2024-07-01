from django.shortcuts import HttpResponse, render
from django.views import View

from network_live.services.excel import create_excel
from network_live.services.select import select_data
from services.mixins import LoginMixin


class NetworkLive(LoginMixin, View):
    """A view for cell data choose and download."""

    template_name = 'network_live/index.html'

    def get(self, request):
        """Handle GET request."""
        return render(request, self.template_name)

    def post(self, request):
        """Handle POST request."""
        technologies = request.POST.getlist('technologies[]')
        network_live_data = select_data(technologies)
        file_path = create_excel(network_live_data)

        file_name = 'kcell' + '_'.join(technologies) + '_data.xlsx'

        with open(file_path, 'rb') as attachment:
            file_data = attachment.read()
            response = HttpResponse(file_data, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
            return response
