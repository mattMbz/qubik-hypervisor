import asyncio, json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from app_tlk.tlk.utilities.hypervisor import Hypervisor
from app_hypervisor.models import VirtualMachine


class WSConsumer(AsyncWebsocketConsumer):
    
    hypervisor = Hypervisor()

    async def connect(self):
        await self.accept()
        self.connected = False
        self.sending_task = None


    async def receive(self, text_data):
        ''' 
         _ If the client sends 'cpu', it starts sending Real-time % CPU usage data.
         _ If the client sends 'ram', it starts sending real time RAM usage data.
         _ If the client sends 'disk',it starts sending Disk usage data.
        '''
        
        mssg = text_data
        
        if mssg == 'stop':
            # if client send 'stop'
            if self.connected:
                self.connected = False
                await self.close()
            
            if self.sending_task:
                self.sending_task.cancel()
        
        elif mssg == 'cpu':
            if not self.connected:
                self.connected = True
                self.connect()
                self.sending_task = asyncio.ensure_future(self.send_cpu_data())

        elif mssg == 'ram':
            if not self.connected:
                self.connected = True
                self.connect()
                self.sending_task = asyncio.ensure_future(self.send_memory_data())

        elif mssg == 'disk':
            if not self.connected:
                self.connected = True
                self.connect()
                self.sending_task = asyncio.ensure_future(self.send_disk_data())

    async def send_cpu_data(self):
        while True:    
            cpu_usage = self.hypervisor.cpu.read()
            print(cpu_usage)
            await self.send(json.dumps(cpu_usage))
            await asyncio.sleep(0.05)


    async def send_memory_data(self):
        while True:
            memory_usage = self.hypervisor.memory.read()
            print(memory_usage)
            await self.send(json.dumps( memory_usage ))
            await asyncio.sleep(10)


    async def send_disk_data(self):
        while True:
            disk_usage = self.hypervisor.disk.read()
            print(disk_usage)
            await self.send(json.dumps( disk_usage ))
            await asyncio.sleep(10)


class VMResourcesConsumer(AsyncWebsocketConsumer):
    
    hypervisor = Hypervisor()

    async def connect(self):
        await self.accept()
        self.connected = False
        self.sending_task = None


    async def get_vm_name(self, vm_id):
        vm = await self.get_vm_instance(vm_id)
        return vm.name
    

    def get_vm_ipv4(self, vm_name):
        vm_ipv4 = self.hypervisor.vm_ipv4_address(vm_name)
        return vm_ipv4


    @sync_to_async
    def get_vm_instance(self, vm_id):
        return VirtualMachine.objects.get(id=vm_id)


    async def receive(self, text_data):

        ''' 
         _ Receive text_data like 'vcpu-b9fcf50041d8463ab37baf106d5f2907' that means <action>-<vm_uuid>.
           the action must be messages as 'stop', 'vcpu', 'vram' or 'vdisk'.
         _ if the client sends 'stop', its starts to run hypervisor funcionality for halt Real-time data.
         _ If the client sends 'vcpu', it starts sending virtual machine Real-time CPU usage data.
         _ If the client sends 'vram', it starts sending virtual machine Real-time RAM usage data.
         _ If the client sends 'vdisk',it starts sending virtual machine Real-time Disk usage data.
        '''

        if len(text_data.split('-')) > 1:
            text_data = text_data.split('-')
            mssg = text_data[0]
            vm_id = text_data[1]
            
            # Obtén el nombre de la máquina virtual asincrónicamente
            vm_name = await self.get_vm_name(vm_id)
        
            # Llama a vm_ipv4_address de forma asincrónica
            vm_ipv4 = self.get_vm_ipv4(vm_name)
        
            print(vm_name, vm_ipv4)
        else:
            mssg = text_data
        
        
        if mssg == 'stop': # if client send 'stop'
            if self.connected:
                self.connected = False
                await self.close()
            
            if self.sending_task:
                self.sending_task.cancel()
                    
        elif mssg == 'vcpu':
            if not self.connected:
                self.connected = True
                self.connect()
                self.sending_task = asyncio.ensure_future(self.send_virtualCPU_data(vm_ipv4))

        elif mssg == 'vram':
            if not self.connected:
                self.connected = True
                self.connect()
                self.sending_task = asyncio.ensure_future(self.send_virtualMemory_data(vm_ipv4))

        elif mssg == 'vdisk':
            if not self.connected:
                self.connected = True
                self.connect()
                self.sending_task = asyncio.ensure_future(self.send_virtualDisk_data(vm_ipv4))
 

    async def send_virtualCPU_data(self, vm_ipv4):
        print(f"Obtener datos de {vm_ipv4}")
        while True:
            cpu_usage = self.hypervisor.vm_cpu_usage(vm_ipv4)
            await self.send(json.dumps( cpu_usage ))
            await asyncio.sleep(0.5)


    async def send_virtualMemory_data(self, vm_ipv4):
        print(f"Obtener datos de {vm_ipv4}")
        while True:
            memory_usage = self.hypervisor.vm_memory_usage(vm_ipv4)
            await self.send(json.dumps( memory_usage ))
            await asyncio.sleep(10)


    async def send_virtualDisk_data(self, vm_ipv4):
        print(f"Obtener datos de {vm_ipv4}")
        while True:
            disk_usage = self.hypervisor.vm_disk_usage(vm_ipv4)
            await self.send(json.dumps( disk_usage ))
            await asyncio.sleep(10)
