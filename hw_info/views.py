from django.shortcuts import HttpResponse, render
from django.views import View

from hw_info.services.excel import create_hw_excel
from hw_info.services.select import select_hw_data
from services.mixins import GroupRequiredMixin, LoginMixin


class HwInfo(LoginMixin, GroupRequiredMixin, View):
    """View to handle requests for the hw_info app."""

    template_name = 'hw_info/index.html'
    required_groups = ['RNPO Users', 'Hardware']

    def get(self, request):
        """Handle GET request."""
        return render(request, self.template_name)

    def post(self, request):
        """Handle POST requests."""
        selected_data = select_hw_data()
        tr_data = create_hw_excel(*selected_data)
        content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        file_name = 'hw-info.xlsx'

        response = HttpResponse(tr_data, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'

        return response
