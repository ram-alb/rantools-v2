import json
from datetime import date
from http import HTTPStatus

import requests
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from services.mixins import GroupRequiredMixin, LoginMixin
from toa_submit.forms import SearchForm
from toa_submit.services.utils import (
    CABINET_TYPE_DICT,
    get_common_data,
    get_dictionary_by_ldap,
    get_site_information,
    get_technology_data,
)

TOA_GSM_WCDMA_URL = "http://alarm.kcell.kz:8000/api/send-toa-23g"
TOA_LTE_NR_URL = "http://alarm.kcell.kz:8000/api/send-toa-45g"
REQUEST_TIMEOUT = 10


class SearchView(LoginMixin, GroupRequiredMixin, View):
    """View to handle requests for the TOA Submit app."""

    required_groups = ["Integration Team"]
    template_name = "toa_submit/index.html"

    def get(self, request):
        """Handle GET method for get request."""
        form = SearchForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Handle POST method for send request."""
        form = SearchForm(request.POST)
        if form.is_valid():
            sitename = form.cleaned_data['site_name']
            technologies = form.cleaned_data['technologies']

            if isinstance(technologies, str):
                technologies = technologies.split(',')
            site = get_site_information(sitename)
            if site is None:
                messages.error(request, f'Site with name {sitename} was not found')
                context = {
                    'sitename': sitename,
                    'technologies': technologies,
                    'form': form,
                }
            else:
                technologies_str = ",".join(technologies)
                query_params = f"?site_name={sitename}&technologies={technologies_str}"
                site_url = reverse("site_form")
                redirect_url = f"{site_url}{query_params}"
                return redirect(redirect_url)
            return render(request, self.template_name, context)

        # Если форма невалидна, верните ее обратно на страницу
        return render(request, self.template_name, {'form': form})


class SiteView(LoginMixin, GroupRequiredMixin, View):
    """View for displaying the page for send TOA requests."""

    required_groups = ["Integration Team"]
    template_name = "toa_submit/search.html"

    def get(self, request):
        """Handle GET method for rendering the TOA form."""
        sitename = request.GET.get('site_name', '')
        technologies = request.GET.get('technologies', '').split(',')

        site_info = self._prepare_site_info(sitename)
        accepted_list = get_dictionary_by_ldap()
        tech_string = ','.join(technologies)

        data_gsm = get_technology_data(sitename, '2G') if '2G' in tech_string else None
        data_wcdma = get_technology_data(sitename, '3G') if '3G' in tech_string else None
        common_data = get_common_data(sitename)

        context = {
            'accepted_list': accepted_list,
            'technologies': technologies,
            'data_2g': data_gsm,
            'data_3g': data_wcdma,
            'common_data': common_data,
            'today': date.today(),
            'site_info': site_info,
            'site_name': sitename,
            'cabinet_type': CABINET_TYPE_DICT,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Handle POST method for send request."""
        username = request.user.email
        action = request.POST.get('action')

        if not action:
            return self._error('Action is missing')

        if action == 'reset':
            return JsonResponse({'redirect': reverse("search_form")})

        if action == 'send_toa':
            return self._handle_send_toa(request, username)

    def _prepare_site_info(self, sitename):
        """Fetch and enrich site information."""
        site_info = get_site_information(sitename)
        payload = {
            "latitude": site_info.get("latitude"),
            "longitude": site_info.get("longitude"),
        }

        try:
            response = requests.post(
                "http://alarm.kcell.kz:8000/get-kato",
                json=payload,
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            response_data = response.json()
        except requests.RequestException:
            response_data = {}

        if site_info.get("address") == 'no address by ATOLL':
            site_info["address"] = response_data.get("address", '')

        site_info["kato"] = response_data.get("kato_id", '')
        site_info["sitename"] = sitename

        return {
            key: (item_val if item_val is not None else '')
            for key, item_val in site_info.items()
        }

    def _handle_send_toa(self, request, username):
        raw_data = request.POST.get('toaData')
        if not raw_data:
            return self._error('toa_data is missing')

        try:
            parsed_data = json.loads(raw_data)
        except json.JSONDecodeError:
            return self._error('Invalid JSON')

        if not isinstance(parsed_data, list):
            return self._error('toa_data is not a valid list')

        response_list = []
        for record in parsed_data:
            record['username'] = username
            response = self._send_request(record)

            if response and response.status_code == HTTPStatus.OK:
                response_list.append({
                    'technology': record['technology'],
                    'band': record.get('band', '2G or 3G'),
                    'success': 'Success',
                })
            else:
                response_list.append({
                    'technology': record.get('technology', 'Unknown'),
                    'band': record.get('band', 'Unknown'),
                    'success': 'Failed',
                })
        return JsonResponse({
            'status': 'success',
            'data': response_list,
            'redirect_url': reverse("search_form"),
        })

    def _send_request(self, record):
        technology = record.get('technology')
        if technology in {'2G', '3G'}:
            url = TOA_GSM_WCDMA_URL
        else:
            url = TOA_LTE_NR_URL

        try:
            return requests.post(url, json=record, timeout=REQUEST_TIMEOUT)
        except requests.RequestException:
            return None

    def _error(self, message):
        return JsonResponse({'error': message}, status=HTTPStatus.BAD_REQUEST)
