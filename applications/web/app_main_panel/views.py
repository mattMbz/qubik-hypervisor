from utils.validations import no_cache_render

from app_hypervisor.models import VirtualMachine

def main_panel(request):
    context = {
        'virtual_machines' : VirtualMachine.objects.all()
    }
    return no_cache_render(request, 'app_main_panel/main.html', context=context)
    # return render(request, 'app_main_panel/main.html', {})