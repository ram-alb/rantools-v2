from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from enm_bulk_config.services.templates import generate_bulk_template


class EnmBulkConfigView(View):
    """View for handling ENM bulk configuration."""

    template_name = "enm_bulk_config/index.html"

    def get(self, request, *args, **kwargs):
        """Handle GET requests for the ENM bulk configuration page."""
        tehnologies = ["LTE", "NR"]
        tech_parameters = {
            "LTE": ["PCI", "RACH", "TAC", "CellId"],
            "NR": ["PCI", "RACH", "TAC", "CellId"],
        }
        context = {
            "technologies": tehnologies,
            "parameters": tech_parameters,
        }

        return render(request, self.template_name, context)


def download_template(request):
    """Download an Excel template for bulk configuration."""
    technology = request.GET.get("technology")
    parameter = request.GET.get("parameter")
    error_status = 400
    if not technology or not parameter:
        return HttpResponse(
            "Invalid technology or parameter selected",
            status=error_status,
        )

    template_content = generate_bulk_template(technology, parameter)
    filename = f"{technology}_{parameter}_template.xlsx"
    response = HttpResponse(
        template_content,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
