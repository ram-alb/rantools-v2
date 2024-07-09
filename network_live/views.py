from django.shortcuts import HttpResponse, render
from django.views import View

from network_live.forms import SelectTables
from network_live.services import excel, select
from services.mixins import GroupMixin, LoginMixin


class NetworkLive(GroupMixin, LoginMixin, View):
    """A view for technology choose and cell data download."""

    template_name = 'network_live/index.html'

    def get(self, request):
        """Handle GET requests to render the form."""
        form = SelectTables()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Handle POST requests to process form submission."""
        form = SelectTables(request.POST)

        if form.is_valid():
            technologies = request.POST.getlist('technologies[]')

            if not technologies:
                err = "Choose at least one technology."
                return render(request, self.template_name, {'form': form, 'error_message': err})

            network_live_data = select.select_data(technologies)
            file_path = excel.create_excel(network_live_data)

            file_name = 'kcell_' + '_'.join(technologies) + '_data.xlsx'

            with open(file_path, 'rb') as attachment:
                file_data = attachment.read()
                response = HttpResponse(file_data, content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                return response

        return render(request, self.template_name, {'form': form})
