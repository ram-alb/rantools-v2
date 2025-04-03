from django.contrib import messages
from django.http import FileResponse
from django.shortcuts import render
from django.views import View

from retsubunit.forms import SearchForm
from retsubunit.services.excel import save_retsubunits_to_excel
from retsubunit.services.retsubunit import get_retsubunits
from services.mixins import GroupRequiredMixin, LoginMixin


class RetSubUnitView(LoginMixin, GroupRequiredMixin, View):
    """View to handle requests for the RetSubUnit app."""

    required_groups = ["RNPO Users"]
    template_name = "retsubunit/index.html"

    def get(self, request):
        """Handle GET requests."""
        search_form = SearchForm()
        return render(request, self.template_name, {"search_form": search_form})

    def post(self, request):
        """Handle POST requests."""
        action = request.POST.get("action")

        if action == "check":
            search_form = SearchForm(request.POST)
            if not search_form.is_valid():
                return render(request, self.template_name, {"search_form": search_form})
            site = search_form.cleaned_data["query"]
            retsubunit_data = get_retsubunits(site)
            if not retsubunit_data:
                messages.error(
                    self.request,
                    f"RetSubUnit Data for site with id {site} was not found",
                )
            return render(
                request,
                self.template_name,
                {"search_form": search_form, "retsubunit_data": retsubunit_data},
            )
        elif action == "download":
            retsubunit_data = get_retsubunits()
            if not retsubunit_data:
                messages.error(request, "No RetSubUnit data available for download.")
                return render(
                    request,
                    self.template_name,
                    {"search_form": SearchForm()},
                )

            retsubunit_excel = save_retsubunits_to_excel(retsubunit_data)
            return FileResponse(
                retsubunit_excel,
                as_attachment=True,
                filename="RetSubUnit.xlsx",
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
