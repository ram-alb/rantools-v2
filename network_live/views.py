import os

from django.shortcuts import HttpResponse, render
from django.views import View

from services.mixins import LoginMixin
from .services.select import select_data
from .services.excel import create_excel


class NetworkLive(LoginMixin, View):

    template_name = 'network_live/index.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        technologies = request.POST.getlist('technologies[]')
        network_live_data = select_data(technologies)
        file_path = create_excel(network_live_data)
        
        # Generate filename based on technologies
        filename = 'kcell' + '_'.join(technologies) + '_data.xlsx'
        
        with open(file_path, 'rb') as attachment:
            file_data = attachment.read()
            response = HttpResponse(file_data, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
            return response