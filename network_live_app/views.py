from django.shortcuts import HttpResponse, render
from django.views import View

from network_live_app.services.excel import create_excel
from network_live_app.services.select import select_data
from services.mixins import GroupRequiredMixin, LoginMixin


class NetworkLive(LoginMixin, GroupRequiredMixin, View):
    """View to handle requests for the network_live app."""

    required_groups = ['RNPO Users']
    template_name = 'network_live/index.html'

    def get(self, request):
        """Handle GET requests."""
        return render(request, self.template_name)

    def post(self, request):
        """Handle POST requests."""
        technologies = request.POST.getlist('technologies')

        network_live_data = select_data(technologies)
        excel_content = create_excel(network_live_data)

        content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        file_name = 'nl_cells.xlsx'

        response = HttpResponse(excel_content, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'

        return response
