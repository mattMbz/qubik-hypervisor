import re
from django import forms


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
        required=False,
        label='Application Name',
        max_length=20,
        widget= forms.TextInput(
            attrs = {
                "autocomplete": "off",
                "class": "form-control",
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

    hardware_choices = [
        ('Debian Linux : 1', 'Debian Linux | 2 CPU | 768 MB (RAM) | 4 GB (Disk)'),
        ('Alpine Linux : 2', 'Alpine Linux | 2 CPU | 768 MB (RAM) | 1 GB (Disk)'),
        ('Alpine Linux : 3', 'Alpine Linux | 2 CPU | 768 MB (RAM) | 2 GB (Disk)'),
    ]

    hardware = forms.ChoiceField(
        required=False,
        choices=hardware_choices,
        label='Select Hardware',
        widget=forms.Select(
            attrs = {
                "class": "form-select",
                "id": 'hardware'
            }
        )
    )


    def clean_virtualMachineName(self):
        virtualMachineName = self.cleaned_data['virtualMachineName']
        pattern = r'^[a-zA-Z0-9]+([_-][a-zA-Z0-9]+)*$'
        if not re.match(pattern, virtualMachineName):
            raise forms.ValidationError("ERROR: The virtual machine name should only contain letters (uppercase or lowercase and numbers with pattern (0-9) (Ex. 'my-vm1025', 'python-virtual-machine'). Try another name! ")
        return virtualMachineName
    #End_def

#End_class