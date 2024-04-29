from django.contrib.auth.models import User

from utils.validations import no_cache_render

from app_hypervisor.models import VirtualMachine


def main_panel(request):

    user = request.user

    context = {}

    if user.is_authenticated:
        username = user.username
        user = User.objects.get(username=username)
        context = {
            'virtual_machines' : VirtualMachine.objects.filter(user=user)
        }
    
    return no_cache_render(request, 'app_main_panel/main.html', context=context)

#End_def