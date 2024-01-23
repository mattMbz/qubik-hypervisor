import json

from utils.validations import no_cache_render

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.generic import View

from app_hypervisor.models import VirtualMachine


class SetupVirtualMachine(View):

    def post(self, request, vm_uuid):
        data = json.loads(request.body)
        print(data)
        context = {
            'status': True,
            'content': 'successfully'
        }

        return JsonResponse(context)

    def get(self, request):
        user = request.user
        context = {}
        if user.is_authenticated:
            username = user.username
            user = User.objects.get(username=username)
            context = {
                'virtual_machines' : VirtualMachine.objects.filter(user=user)
            }
            return no_cache_render(request, 'app_hypervisor/setup_vm.html', context=context)
        
        #return no_cache_render(request, 'app_hypervisor/setup_vm.html', context=context)