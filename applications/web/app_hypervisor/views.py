# Django utilities
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import redirect

# Own libraries and functions
from utils.validations import no_cache_render, uuid_letter_prefix
from app_tlk.tlk.utilities.hypervisor import Hypervisor

# Custom form
from .forms import CreateVirtualMachineForm

# hypervisor app models
from .models import VirtualMachine, Resources, Services


## app_hypervisor application views
hypervisor = Hypervisor()


@login_required
def monitor(request):
    context = {
        'resources': hypervisor.getHypervisorResources(),
        'cores': [ f"CPU {n}" for n in range(hypervisor.cpu.get_cores())]
    }
    return no_cache_render(request, 'app_hypervisor/monitor.html', context=context)


@login_required
def tasks(request):
    return no_cache_render(request, 'app_hypervisor/tasks.html', {})


@login_required
def create_virtual_machine(request):
    if request.method == 'POST':
        form = CreateVirtualMachineForm(request.POST)
        if form.is_valid():
            # Procesa los datos del formulario aquí
            virtual_machine_name = form.cleaned_data['virtualMachineName']
            application_name = form.cleaned_data['applicationName']
            version = form.cleaned_data['version']
            hardware = form.cleaned_data['optradio']

            number_service_chosen = hardware.split(":")[1]
            number_service_chosen = number_service_chosen.strip()

            chosen_service = Services.objects.get(choice=hardware)
            chosen_resources = chosen_service.description.split("|")
            chosen_vm_resources = [ resource.strip() for resource in chosen_resources ]

            user = request.user

            if user.is_authenticated:
                new_vm_resources = Resources.objects.create(
                    os=chosen_vm_resources[0],
                    vcpu=chosen_vm_resources[1],
                    vram=chosen_vm_resources[2],
                    vdisk=chosen_vm_resources[3]
                )

                vm_user =  User.objects.get(username=user.username)
                VirtualMachine.objects.create(
                    id = uuid_letter_prefix(),
                    name = virtual_machine_name,
                    app_name = application_name,
                    app_version = version,
                    user = vm_user,
                    resources = new_vm_resources,
                    creation_date = timezone.now()
                )

                chosen_service.users.add(vm_user)

                ''' 
                Create new virtual machine for this User
                this take three parameters:
                    1. Name for virtual machine
                    2. Operating system name
                    3. Option choice, is a number
                '''
                hypervisor.createNewVirtualMachine (
                    virtual_machine_name, 
                    chosen_vm_resources[0], 
                    number_service_chosen,
                    application_name,
                    user.username
                )

                messages.success(request, '&#128516; New virtual machine has been created successfully! ')

                return redirect('create-vm')
    else:
        form = CreateVirtualMachineForm()

    return no_cache_render(request, 'app_hypervisor/create_vm.html', {'form': form})


@login_required
def start(request, vm_uuid):
    virtual_machine = VirtualMachine.objects.get(id=vm_uuid)
    virtual_machine.state = True
    virtual_machine.save()
    hypervisor.startVM(virtual_machine.name)

    return JsonResponse({'status':f'{vm_uuid}'})


@login_required
def status(request, vm_uuid):
    virtual_machine = VirtualMachine.objects.get(id=vm_uuid)
    vmname = virtual_machine.name
    vm_ip_address = hypervisor.vm_ipv4_address(vmname)
    checked = hypervisor.vm_check_status(vm_ip_address)

    return JsonResponse(checked)


@login_required
def shutdown(request, vm_uuid):
    virtual_machine = VirtualMachine.objects.get(id=vm_uuid)
    virtual_machine.state = False
    virtual_machine.save()
    hypervisor.shutdownVM(virtual_machine.name)
    
    return JsonResponse({'status':f'{vm_uuid}'})


@login_required
def delete(request, vm_uuid=None):
    if vm_uuid is None and request.method=='GET':
        
        user = request.user

        if user.is_authenticated:
            context = {
                'virtual_machines': VirtualMachine.objects.filter(user=user)
            }
            return no_cache_render(request, 'app_hypervisor/delete_vm.html', context=context)
    
    elif request.method=='DELETE':
        user = request.user

        try:
            virtual_machine = VirtualMachine.objects.get(id=vm_uuid)
            
            if virtual_machine.name in hypervisor.getNamesOfRunningVM():
                return JsonResponse(
                    {
                        'status':'error', 
                        'message':f"The virtual Machine called '{virtual_machine.name}' cannot be delete. Because it's running. Please, shutdown first!"
                    }
                )
            else:

                # Remove from Hypervisor register
                hypervisor.deleteVM(virtual_machine.name, virtual_machine.id, user.username)
                
                # Remove from database
                virtual_machine.delete()

                return JsonResponse({'status':f'{vm_uuid}', 'message':'Virtual Machine deleted successfully'})
        
        except VirtualMachine.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Error'})
