# Python utilities
import os, re, inquirer
from prettytable import PrettyTable

# TLK imports
from tlk.utilities.hypervisor import Hypervisor
from tlk.utilities.screen import RealTimeScreen as rts

class CustomMenu():
    ''' '''
    def __init__(self) -> None:
        self.input = MenuInput()
    #End_def

    def show(self, header, items):
        '''Create the option menu'''

        while True:
            # Print the menu header
            print("+====================================+")

            for i in range(len(header)):
                print(f"| {header[i]:34} |")

            print("+====================================+")
            print("|  Menu options:                     |")
            print("+====================================+")

            # Print the menu items
            for i in range(len(items)):
                print(f"|  {i+1}. {items[i]:30} |")

            print("+====================================+")
            
            #Write your code here ...
            self.input.starts()

            response=input("Confirm exit? (y/N): ")
            if(self.exit(response)):
                break
            else:
                os.system('clear')
    #End_def

    def exit(self, response):
        ex=True
        default_regex = r"^(\s+)?$"
        response=response.lower()
        if re.match(default_regex, response):
            ex=False
        else:
            if response == 'n' or response == 'no':
                ex=False
            elif response == 'y' or response == 'yes':
                ex=True
            else:
                ex=False
        return ex
    #End_of_def

#### End_class


class MenuInput():
    ''' '''
    def __init__(self) -> None:
        self.process = Process()
    #End_def
    
    def starts(self):
        option = input("Enter an option: ")
        print("\n")
        self.process.run(option)
    #End_def

#### End_Class


class Process():

    def __init__(self) -> None:
        self.output = MenuOutput()
        self.qubik = Hypervisor()
        self.keyword = '.cancel'
    #End_def


    def run(self, option):

        # Option 1 is when we want create new virtual machine
        if option == "1":
            
            print("Creating new virtual machine")
        
            vm_question = [inquirer.Text('vmname',  message='Input the name of new VM')]
            vm_answers = inquirer.prompt(vm_question)
            virtual_machine_name = vm_answers['vmname']
            print(virtual_machine_name)

            os_options  = ['Debian Linux', 'Alpine Linux']
            os_options.append(self.keyword)
            os_question = [inquirer.List(
                'os',
                message = 'Select the Operating System:',
                choices = os_options
            )]
            os_answers = inquirer.prompt(os_question)
            operating_system = os_answers['os']
            print(operating_system)
           
            if operating_system != self.keyword:
                ram_cpu_options = []

                if operating_system == os_options[0]:
                    os = os_options[0]
                    ram_cpu_options = [
                        f'1| {os} | 1 CPU | 512 MB (RAM) |  2 GB (Disk)',
                        f'2| {os} | 2 CPU | 768 MB (RAM) |  4 GB (Disk)',
                        f'3| {os} | 3 CPU | 768 MB (RAM) |  4 GB (Disk)',
                        f'4| {os} | 4 CPU |   2 GB (RAM) |  8 GB (Disk)',
                        f'5| {os} | 4 CPU |   4 GB (RAM) | 10 GB (Disk)',
                    ]
                else:
                    os = os_options[1]
                    ram_cpu_options = [
                        f'1| {os} | 1 CPU | 256 MB (RAM) | 1 GB (Disk)',
                        f'2| {os} | 2 CPU | 768 MB (RAM) | 1 GB (Disk)',
                        f'3| {os} | 2 CPU | 768 MB (RAM) | 2 GB (Disk)',
                        f'4| {os} | 4 CPU |   2 GB (RAM) | 4 GB (Disk)',
                        f'5| {os} | 2 CPU |   2 GB (RAM) | 4 GB (Disk)',
                    ]
            
                ram_cpu_options.append(self.keyword)
            
                vm_resources_question = [inquirer.List(
                    'resources',
                    message = 'Select CPU, RAM and Disk size:',
                    choices = ram_cpu_options
                )]
                vm_resources_answers = inquirer.prompt(vm_resources_question)
                vm_resources = vm_resources_answers['resources']
            
                resource_options = vm_resources.split('|')[0]
             
                if vm_resources != self.keyword:
                    if self.parse_vm_name(virtual_machine_name):
                        self.qubik.createNewVirtualMachine(virtual_machine_name, operating_system, resource_options)

            # self.output.starts(vm_name)
        
        elif option == "2":
            print("Removing virtual machine")
            print(self.qubik.getVirtualMachineNames())
            questions = [inquirer.Text('input', message="Input VM name to remove")]
            
            answers = inquirer.prompt(questions)
            vm_name = answers['input']
            print()
            if(vm_name!=self.keyword.lower()):
                self.qubik.deleteVM(vm_name)
                #executeFile(PATH, 'remove-vm.sh', vm_name)
        
        elif option == "3":
            print("Replacing virtual machine name ...")
            
            self.show_pretty_list()

            vm_question = [inquirer.Text('vmname',  message='Input VM name to replace')]
            vm_answers = inquirer.prompt(vm_question)
            virtual_machine_name = vm_answers['vmname']
        
            if(virtual_machine_name != self.keyword.lower()):
                new_vm_question = [inquirer.Text('new_vm_name', message="Input new VM name")]            
                new_vm_answers = inquirer.prompt(new_vm_question)
                new_vm_name = new_vm_answers['new_vm_name']
                if(new_vm_name != self.keyword.lower()):
                    self.qubik.renameVM(virtual_machine_name, new_vm_name)

        elif option == "4":
            print("Starting virtual machine ...")
            choiceValues = self.qubik.getStoppedVM()
            choiceValues.append(self.keyword)
            questions = [
                inquirer.List(
                    'option',
                    message="Select any option",
                    choices=choiceValues
                )
            ]
            answers = inquirer.prompt(questions)
            vm_name = answers['option']
            print()
            print(f'has seleccionado {vm_name}')

            if(vm_name != self.keyword.lower()):
                #executeFile(PATH, 'start-vm.sh', vm_name)
                self.qubik.startVM(vm_name)

        elif option == "5":
            print("Shutting down virtual machine ...")
            choiceValues = self.qubik.getNamesOfRunningVM()
            choiceValues.append(self.keyword)
            questions = [
                inquirer.List(
                    'option',
                    message="Select any option",
                    choices=choiceValues
                ),
            ]
            answers = inquirer.prompt(questions)
            selected_options = answers['option']
            
            print()
            if(selected_options != self.keyword.lower()):
                #executeFile(PATH, 'shutdown-vm.sh', selected_options)
                self.qubik.shutdownVM(selected_options)
                
        elif option == "6":
            print("Your virtual machines: ")
            print()
            vm_list =  self.qubik.listVirtualMachines()
            table = PrettyTable()
            table.field_names = ["Id","Virtual Machine","State"]
            for vm in vm_list:
                table.add_row([value for value in vm.values()])
            print(table)

        elif option == "7":
            resources_rts = rts() # Creating RealTimeScreen Instance
            resources_rts.cursesWrapper()
            print(" Hypervisor monitor has finished !")
            print()

        elif option == "8":
            print("Goodbye!")
        
        else:
            print("Invalid option, please enter a valid option !")
    #End_def


    def parse_vm_name(self, vm_name):
        response=False
        vm_name=vm_name.lower()

        regex = r"^(?!.*\.{2,})[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*$"

        if re.match(regex, vm_name):
            response=True
        else:
            self.message(1)
        return response
    #End_def


    def show_pretty_list(self, ):
        self.qubik = Hypervisor()
        vm_list =  self.qubik.listVirtualMachines()
        table = PrettyTable()
        table.field_names = ["Id","Virtual Machine","State"]
        for vm in vm_list:
            table.add_row([value for value in vm.values()])
        print(table)
    #End_def


    def message(self, code):
        if code==1:
            print('Invalid name, try without simbols!')
    #End_def

#### End_class


class MenuOutput():

    def __init__(self) -> None:
        pass
    #End_def

    def starts(self, option):
        print(f'The output was: {option}')
    #End_def

#### End_Class

## END
