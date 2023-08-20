# Python Utitlities
import libvirt, os
from dotenv import load_dotenv

# TLK imports
from app_tlk.tlk.utilities.bash import executeFile, executeFileWithReturn
from app_tlk.tlk.utilities.resources import Memory, Disk, CPU
from app_tlk.tlk.utilities.socketClient import get_vm_resources

# Global variables and paths
load_dotenv()
PATH = os.getenv('PATH_TO_SCRIPT')
PORT = int(os.getenv('WS_PORT'))

class Hypervisor:
    '''Implementing Libvirt functionalities for managing virtual machines '''

    def __init__(self):
        self.conn = libvirt.open('qemu:///system')
        self.memory = Memory()
        self.disk = Disk()
        self.cpu = CPU()

        if self.conn == None:
            print('Hypervisor conection Failed!')
            exit(1)

    
    def createNewVirtualMachine(self, vmname, operating_system, resource_options):
       """ 
        Create new virtual machine

        Args: 
            vmname (str): Virtual machine name
            operating_system (str): Linux distribution
            resource_options (str): Option number for resources (CPU, RAM and Disk)

        Returns: 
       """

       clone_options = {
            'Debian Linux': { 
                '1': 'debianBase-1vcpu-512mb-2gb-vm', #1 CPU | 512 MB (RAM) |  2 GB (Disk)
                '2': 'debianBase-2vcpu-768mb-4gb-vm', #2 CPU | 768 MB (RAM) |  4 GB (Disk)
                '3': 'debianBase-3vcpu-768mb-4gb-vm', #3 CPU | 768 MB (RAM) |  4 GB (Disk)
                '4': 'debianBase-4vcpu-2gb-8gb-vm',   #4 CPU |   2 GB (RAM) |  8 GB (Disk)
                '5': 'debianBase-4vcpu-4gb-10gb-vm'   #4 CPU |   4 GB (RAM) | 10 GB (Disk)
            },
            'Alpine Linux': {
                '1': 'alpineBase-1vcpu-256mb-1gb-vm', #1 CPU | 256 MB (RAM) | 1 GB (Disk)
                '2': 'alpineBase-2vcpu-768mb-1gb-vm', #2 CPU | 768 MB (RAM) | 1 GB (Disk)
                '3': 'alpineBase-2vcpu-768mb-2gb-vm', #2 CPU | 768 MB (RAM) | 2 GB (Disk)
                '4': 'alpineBase-2vcpu-2gb-4gb-vm',   #4 CPU |   2 GB (RAM) | 4 GB (Disk)
                '5': 'alpineBase-4vcpu-2gb-4gb-vm'    #2 CPU |   2 GB (RAM) | 4 GB (Disk)
            },
       }

       if (operating_system=='Debian Linux' and resource_options=='2'):
            clone_option = (clone_options[operating_system][resource_options])
            print(f'clone.sh {clone_option} {vmname}')

            # Execute process from bash
            executeFile(PATH, 'clone-vm.sh', clone_option, vmname)

       elif (operating_system=='Alpine Linux' and ( resource_options=='2' or resource_options=='3' )):
            clone_option = (clone_options[operating_system][resource_options])
            print(f'clone.sh {clone_option} {vmname}')

            # Execute process from bash
            executeFile(PATH, 'clone-vm.sh', clone_option, vmname)

       else:
            print('Not implemented yet !')


    def startVM(self, vmname):
        domain = self.conn.lookupByName(vmname)
        domain.create()
   

    def renameVM(self, oldname, newname):
        '''Rename some virtual machine ''' 
        domains = self.conn.listAllDomains()

        try:
            domain = self.conn.lookupByName(oldname)
            domain.rename(newname)
        except Exception as error:
            print("ERROR: ", type(error).__name__)

   
    def deleteVM(self, vmname):
        '''Delete some virtual machine if exists.'''
        domains = self.getVirtualMachineNames()
        
        if vmname in domains:
           '''vnmane Exists''' 
           domain = self.conn.lookupByName(vmname)

           if domain.state()[0] == 1: 
               print('The VM is running. Please Turn-off first !')
           else:
                # Execute process from bash
                executeFile(PATH, 'remove-vm.sh', vmname)

        else:
            print('That VM  not exists !')    


    def shutdownVM(self,vmname):
        ''' '''
        domain = self.conn.lookupByName(vmname)
        domain.shutdown()


    def listVirtualMachines(self):
        ''' '''
        domains = self.conn.listAllDomains()
        vms = []
        
        for domain in domains:
            state = 'off'
            id = '-'
            
            if domain.state()[0]==1:
                state = 'Runnning' 
            
            if domain.ID() != -1:
                id = domain.ID() 
 
            vms.append({'id': id, 'vmname': domain.name(), 'state': state})
        
        return vms


    def getVirtualMachineNames(self):
        domains = self.conn.listAllDomains()
        onlynames = [] 
        for domain in domains:
            onlynames.append(domain.name())
        
        return onlynames
    
    
    def getNamesOfRunningVM(self):
        active_domains = self.conn.listDomainsID()
        only_actives = []
        for domain_id in active_domains:
            domain = self.conn.lookupByID(domain_id)
            only_actives.append(domain.name())

        if len(only_actives)==0:
            print('There are not Running Virtual Machine, press ENTER to exit!')
    
        return only_actives
            
    
    def getStoppedVM(self):
        defined_domains = self.conn.listDefinedDomains()
        return defined_domains


    def getHypervisorResources(self):
        node_info = self.conn.getInfo()
        return {
            'hostname': os.uname().nodename,
            'os': os.uname().sysname,
            'release': os.uname().release,
            'version': os.uname().version,
            'machine': node_info[0],
            'memory': node_info[1],
            'vcpus': node_info[2]
        }


    def vm_cpu_usage(self, host):
        return get_vm_resources(host, PORT, 'cpu')


    def vm_memory_usage(self, host):
        return get_vm_resources(host, PORT, 'memory')


    def vm_disk_usage(self, host):
        return get_vm_resources(host, PORT, 'disk')


    def vm_check_status(self, host):
        status = get_vm_resources(host, PORT, 'cpu')
        return status


    def vm_ipv4_address(self, vmname):
        ipv4 = executeFileWithReturn(PATH, 'get-vm-ipv4.sh', vmname)
        ip_address = ipv4.strip().replace(" ", "")
        return ip_address
