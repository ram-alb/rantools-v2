from django.shortcuts import HttpResponse, render
from django.views import View

from services.mixins import GroupRequiredMixin, LoginMixin
from tr_data.services.enm import get_sts
from tr_data.services.excel import create_tr_excel
from tr_data.services.select import select_tr_data


class TrData(LoginMixin, GroupRequiredMixin, View):
    """View to handle requests for the tr_data app."""

    required_groups = ['RNPO Users', 'Trans Group']
    template_name = 'tr_data/index.html'

    def get(self, request):
        """Handle GET requests."""
        return render(request, self.template_name)

    def post(self, request):
        """Handle POST requests."""
        action = request.POST.get('action')

        if action == 'sts':
            sts_data = get_sts()
            tr_data = create_tr_excel(*sts_data)
        elif action == 'ip':
            selected_data = select_tr_data()
            tr_data = create_tr_excel(*selected_data)

        content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        file_name = 'tr-data.xlsx'

        response = HttpResponse(tr_data, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'

        return response
