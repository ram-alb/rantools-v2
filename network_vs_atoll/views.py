from django.http import JsonResponse
from django.shortcuts import HttpResponse, render
from django.views import View

from network_vs_atoll.services.excel import write_diffs_to_excel
from network_vs_atoll.services.lte.main import main as lte_main
from services.mixins import GroupRequiredMixin, LoginMixin

BAD_REQUEST = 400


class NetworkVsAtollView(LoginMixin, GroupRequiredMixin, View):
    """View for Network vs Atoll page."""

    required_groups = ['RNPO Users']
    template_name = 'network_vs_atoll/index.html'

    def get(self, request):
        """Handle GET requests."""
        return render(request, self.template_name)

    def post(self, request):
        """Handle POST requests."""
        action = request.POST.get('action')
        if action == 'calculate_diff':
            lte_total_diff_count, lte_diff_count_by_subnetwork, lte_diffs = lte_main()
            request.session['LTE'] = lte_diffs
            return JsonResponse({
                'summary': {'LTE': lte_total_diff_count},
                'summary_by_technologies': {'LTE': lte_diff_count_by_subnetwork},
                'diffs': {'LTE': lte_diffs},
            })

        if action == 'download_excel':
            technology = request.POST.get('technology')
            node = request.POST.get('node')
            diffs = request.session.get(technology)

            if not diffs:
                return HttpResponse("Diffs not found in session", status=BAD_REQUEST)

            try:
                node_diffs = diffs[node]
            except KeyError:
                return HttpResponse("Invalid technology or node", status=BAD_REQUEST)

            diff_excell = write_diffs_to_excel(node_diffs)

            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            file_name = f'{technology}-{node}-diffs.xlsx'
            response = HttpResponse(diff_excell, content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response

        return HttpResponse("Invalid action", status=BAD_REQUEST)
