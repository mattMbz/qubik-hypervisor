from utils.validations import no_cache_render

def setup_virtual_machine(request):
    if request.method == 'POST':
        pass

    return no_cache_render(request, 'app_hypervisor/setup_vm.html', {})