from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from openpyxl import Workbook


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

    # Создаем Excel-файл с двумя колонками: 'cell' и выбранный параметр
    wb = Workbook()
    ws = wb.active
    ws.title = f"{technology}_{parameter}"
    ws.append(["cell", f"new {parameter}"])  # Заголовки столбцов

    # Готовим ответ для скачивания
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    filename = f"{technology}_{parameter}_template.xlsx"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response
