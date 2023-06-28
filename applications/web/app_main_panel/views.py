from utils.validations import no_cache_render
from app_hypervisor.models import virtual_machines



vms = {
    'virtual_machines' : virtual_machines,
    'numbers' : len(virtual_machines)
}

def main_panel(request):
    return no_cache_render(request, 'app_main_panel/main.html', vms)
    # return render(request, 'app_main_panel/main.html', {})