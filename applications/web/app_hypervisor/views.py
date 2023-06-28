from django.shortcuts import redirect

from utils.validations import no_cache_render
from .models import virtual_machines
from .forms import CreateVirtualMachineForm

def monitor(request):
    return no_cache_render(request, 'app_hypervisor/monitor.html', {})


def tasks(request):
    return no_cache_render(request, 'app_hypervisor/tasks.html', {})


def create_virtual_machine(request):
    if request.method == 'POST':
        form = CreateVirtualMachineForm(request.POST)
        print('post form')
        print(form.is_valid())
        if form.is_valid():
            print('is valid !!!')
            # Procesa los datos del formulario aquí
            virtual_machine_name = form.cleaned_data['virtualMachineName']
            application_name = form.cleaned_data['applicationName']
            version = form.cleaned_data['version']
            hardware = form.cleaned_data['hardware']
            
            # Haz algo con los datos, como guardarlos en la base de datos

            # Redirige al usuario a alguna página de éxito
            # return redirect('nombre_app:exito')
    else:
        form = CreateVirtualMachineForm()

    return no_cache_render(request, 'app_hypervisor/create_vm.html', {'form': form})


def delete(request):

    return no_cache_render(request, 'app_hypervisor/delete_vm.html', {
        'virtual_machines': virtual_machines
    })
