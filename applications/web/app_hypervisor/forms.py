import re
from django import forms
from app_hypervisor.models import Services



class CreateVirtualMachineForm(forms.Form):

    virtualMachineName = forms.CharField(
        required=True,
        label='Virtual Machine Name (*)',
        max_length=50,
        error_messages={
            'required': ("* The virtual machine name field is required!"),
        },
        widget= forms.TextInput(
            attrs = {
                "autocomplete": "off",
                "class": "form-control",
                "id": 'virtualMachineName'
            }
        )
    )

    applicationName = forms.CharField(
        required=True,
        label='Application Name (*)',
        max_length=15,
        widget= forms.TextInput(
            attrs = {
                "autocomplete": "off",
                "class": "form-control ",
                "id": 'applicationName'
            }
        )
    )

    version = forms.CharField(
        required=False,
        label='Version',
        max_length=5,
        widget= forms.TextInput(
            attrs = {
                "autocomplete": "off",
                "class": "form-control",
                "id": 'version'
            }
        )
    )

    locationHost = forms.CharField(
        required=False,
        label='Location Host',
        max_length=100, 
        disabled=True,
        widget=forms.TextInput(
            attrs = {
                "autocomplete": "off",
                "class": "form-control",
                "id": 'locationHost'
            }
        )
    )

    def load_choiceField():
        hardware_choices = []
        for service in Services.objects.all().values():
            row = (service['choice'], service['description'])
            hardware_choices.append(row)
        
        return hardware_choices

    optradio = forms.ChoiceField(
        choices=load_choiceField(),
        label='Select VM features & Technologies',
        widget=forms.RadioSelect(
            attrs = {
                'class': 'form-check-input',
                'id': 'radioSelect'
            }
        ),
        initial='Debian Linux : 2',
    )

    def clean_virtualMachineName(self):
        virtualMachineName = self.cleaned_data['virtualMachineName']
        pattern = r'^[a-zA-Z0-9]+([_-][a-zA-Z0-9]+)*$'
        if not re.match(pattern, virtualMachineName):
            raise forms.ValidationError("ERROR: The virtual machine name should only contain letters (uppercase or lowercase and numbers with pattern (0-9) (Ex. 'my-vm1025', 'python-virtual-machine'). Try another name! ")
        return virtualMachineName