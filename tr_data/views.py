from django.shortcuts import HttpResponse, render
from django.views import View

from services.mixins import GroupRequiredMixin, LoginMixin
from tr_data.forms import SearchForm
from tr_data.services.db import FAULT_KEYWORDS, get_sts_data
from tr_data.services.enm import get_enm_sts_live_data
from tr_data.services.enm_parser import parse_node_sts_data
from tr_data.services.excel import create_tr_excel
from tr_data.services.select import select_tr_data


class TrData(LoginMixin, GroupRequiredMixin, View):
    """View to handle requests for the tr_data app."""

    required_groups = ["RNPO Users", "Trans Group"]
    template_name = "tr_data/index.html"

    def get(self, request):
        """Handle GET requests."""
        search_form = SearchForm()
        return render(request, self.template_name, {"search_form": search_form})

    def post(self, request):
        """Handle POST requests."""
        action = request.POST.get("action")

        if action == "sts":
            sts_data = get_sts_data()
            tr_data = create_tr_excel(*sts_data)
        elif action == "ip":
            selected_data = select_tr_data()
            tr_data = create_tr_excel(*selected_data)
        elif action == "check":
            site = request.POST.get("query")
            search_form = SearchForm(request.POST)
            enm_data = get_enm_sts_live_data(site)
            node_sts = parse_node_sts_data(enm_data)
            return render(
                request,
                self.template_name,
                {
                    "search_form": search_form,
                    "node_sts": node_sts,
                    "fault_keywords": FAULT_KEYWORDS,
                },
            )

        content_type = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        file_name = "tr-data.xlsx"

        response = HttpResponse(tr_data, content_type=content_type)
        response["Content-Disposition"] = f'attachment; filename="{file_name}"'

        return response
