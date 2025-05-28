from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from enm_bulk_config.services.templates import generate_bulk_template, validate_uploaded_template


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

    def post(self, request, *args, **kwargs):
        """Handle POST requests for the ENM bulk configuration page."""
        technology = request.POST.get("technology")
        parameter = request.POST.get("parameter")
        template_file = request.FILES.get("template_file")

        tehnologies = ["LTE", "NR"]
        tech_parameters = {
            "LTE": ["PCI", "RACH", "TAC", "CellId"],
            "NR": ["PCI", "RACH", "TAC", "CellId"],
        }
        context = {
            "technologies": tehnologies,
            "parameters": tech_parameters,
            "selected_technology": technology,
            "selected_parameter": parameter,
        }

        if not (technology and parameter and template_file):
            messages.error(
                request,
                "Please select technology, parameter and upload a file.",
            )
            return render(request, self.template_name, context)

        is_valid, error = validate_uploaded_template(template_file, parameter)
        if not is_valid:
            messages.error(request, f"Invalid template: {error}")
            return render(request, self.template_name, context)

        return HttpResponse("Template validated successfully!")


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
