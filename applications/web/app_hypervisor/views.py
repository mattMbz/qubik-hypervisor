# Python utilities
import uuid

# Django utilities
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import redirect

# Own libraries and functions
from utils.validations import no_cache_render

# Custom form
from .forms import CreateVirtualMachineForm

# hypervisor app models
from .models import VirtualMachine, Resources, Services


## app_hypervisor application views

@login_required
def monitor(request):
    return no_cache_render(request, 'app_hypervisor/monitor.html', {})
#End_def


@login_required
def tasks(request):
    return no_cache_render(request, 'app_hypervisor/tasks.html', {})
#End_def


@login_required
def create_virtual_machine(request):
    if request.method == 'POST':
        form = CreateVirtualMachineForm(request.POST)
        if form.is_valid():
            # Procesa los datos del formulario aquí
            virtual_machine_name = form.cleaned_data['virtualMachineName']
            application_name = form.cleaned_data['applicationName']
            version = form.cleaned_data['version']
            hardware = form.cleaned_data['hardware']
            
            chosen_service = Services.objects.get(choice=hardware)
            chosen_resources = chosen_service.description.split("|")
            chosen_vm_resources = [ resource.strip() for resource in chosen_resources ]

            user = request.user

            if user.is_authenticated:
                print(f'USER: {user.username}')

                # Haz algo con los datos, como guardarlos en la base de datos
                print(f'vm name: {virtual_machine_name}')
                print(f'app name: {application_name}')
                print(f'version: {version}')
                print(f'hardware: {hardware}')

                new_vm_resources = Resources.objects.create(
                    os=chosen_vm_resources[0],
                    vcpu=chosen_vm_resources[1],
                    vram=chosen_vm_resources[2],
                    vdisk=chosen_vm_resources[3]
                )

                print(new_vm_resources)

                vm_user =  User.objects.get(username=user.username)
                VirtualMachine.objects.create(
                    id = uuid.uuid1(),
                    name = virtual_machine_name,
                    app_name = application_name,
                    user = vm_user,
                    resources = new_vm_resources,
                    creation_date = timezone.now()
                )

                chosen_service.users.add(vm_user)

                # Redirige al usuario a alguna página de éxito
                messages.success(request, '&#128516; New virtual machine has been created successfully! ')
                # go_to_url = reverse('mainpanel')
                # go_to_message = f"Go to <a href='{go_to_url}'>Main panel</a>"
                # messages.success(request, go_to_message, extra_tags='safe')
                return redirect('create-vm')
    else:
        form = CreateVirtualMachineForm()

    return no_cache_render(request, 'app_hypervisor/create_vm.html', {'form': form})
#End_def


@login_required
def remove(request, vm_uuid=None):
    if vm_uuid is None and request.method=='GET':
        
        user = request.user
        username = user.username

        if user.is_authenticated:
            context = {
                'virtual_machines': VirtualMachine.objects.filter(user=user)
            }
            return no_cache_render(request, 'app_hypervisor/remove_vm.html', context=context)
    
    elif request.method=='DELETE':
        try:
            virtual_machine = VirtualMachine.objects.get(id=uuid.UUID(vm_uuid))
            virtual_machine.delete()
            print(f'Deleted >> {vm_uuid}')
            return JsonResponse({'status':f'{vm_uuid}', 'message':'Virtual Machine deleted successfully'})
        except VirtualMachine.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Error'})
#End_def