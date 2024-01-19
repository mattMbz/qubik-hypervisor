from django import forms
from django.forms import Select

from app_hypervisor.models import VirtualMachine

class SetupVirtualMachineForm(forms.Form):

    def load_choiceField():
        # vm_choices = []
        vm_choices = [('Select your vm', (('','vm001'),('','vm002')) )]
        # for vm in VirtualMachine.objects.all().values():
        #     row = (vm['name'], vm['name'])
        #     vm_choices.append(row)
        

        return vm_choices
    

    virtualMachine = forms.ChoiceField(
        required=True,
        choices=load_choiceField(),
        label='Choose your Virtual Machine',
        widget=forms.Select(
            attrs = {
                "class": "form-select",
                "id": "vm-setup",
            }
        ),
    )
