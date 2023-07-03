from django.contrib import messages
from django.shortcuts import redirect

from utils.validations import no_cache_render
from .forms import CreateVirtualMachineForm

def monitor(request):
    return no_cache_render(request, 'app_hypervisor/monitor.html', {})


def tasks(request):
    return no_cache_render(request, 'app_hypervisor/tasks.html', {})


def create_virtual_machine(request):
    if request.method == 'POST':
        form = CreateVirtualMachineForm(request.POST)
        if form.is_valid():
            # Procesa los datos del formulario aquí
            virtual_machine_name = form.cleaned_data['virtualMachineName']
            application_name = form.cleaned_data['applicationName']
            version = form.cleaned_data['version']
            hardware = form.cleaned_data['hardware']
            
            # Haz algo con los datos, como guardarlos en la base de datos
            print(f'vm name: {virtual_machine_name}')
            print(f'app name: {application_name}')
            print(f'version: {version}')
            print(f'hardware: {hardware}')

            # Redirige al usuario a alguna página de éxito
            messages.success(request, '&#128516; New virtual machine has been created successfully! ')
            # go_to_url = reverse('mainpanel')
            # go_to_message = f"Go to <a href='{go_to_url}'>Main panel</a>"
            # messages.success(request, go_to_message, extra_tags='safe')
            return redirect('create-vm')
    else:
        form = CreateVirtualMachineForm()

    return no_cache_render(request, 'app_hypervisor/create_vm.html', {'form': form})


def delete(request):

    return no_cache_render(request, 'app_hypervisor/delete_vm.html', {})
