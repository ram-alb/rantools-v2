from django.shortcuts import render, HttpResponse
from django.views import View
from services.mixins import GroupRequiredMixin, LoginMixin
from network_vs_atoll.services.main import main
from network_vs_atoll.services.excel import fill_excel


class NetworkVsAtollView(View):
    """A view for displaying Network vs Atoll data."""

    diff = {}

    def get(self, request, *args, **kwargs):
        """Handle GET request to display diffs between Network and Atoll."""
        context = {}
        deltas, diff = main()
        context['diff'] = diff

        for tech, delta in deltas.items():
            self.diff[tech] = delta

        return render(request, 'network_vs_atoll/index.html', context)

    def post(self, request, *args, **kwargs):
        """Handle POST request to fille report and send it for download."""
        technology = request.POST.get('technology')
        node = request.POST.get('node')

        report_path = fill_excel(node, self.diff[technology][node])
        with open(report_path, 'rb') as attachment:
            file_data = attachment.read()
            response = HttpResponse(
                file_data,
                content_type='application/vnd.ms-excel',
            )
            response['Content-Disposition'] = (
                f'attachment; filename="{node}.xlsx"'
            )
            return response