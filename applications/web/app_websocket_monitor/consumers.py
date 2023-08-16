import asyncio, json
from channels.generic.websocket import AsyncWebsocketConsumer

from app_tlk.tlk.utilities.hypervisor import Hypervisor


class WSConsumer(AsyncWebsocketConsumer):
    
    hypervisor = Hypervisor()

    async def connect(self):
        await self.accept()
        self.connected = False
        self.sending_task = None
    #End_def


    async def receive(self, text_data):
        ''' 
         - If the client sends 'cpu', it starts sending Real-time % CPU usage data.
         - If the client sends 'ram', it starts sending real time RAM usage data.
         - If the client sends 'disk',it starts sending Disk usage data.
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
    #End_def


    async def send_cpu_data(self):
        while True:    
            cpu_usage = self.hypervisor.cpu.read()
            print(cpu_usage)
            await self.send(json.dumps(cpu_usage))
            await asyncio.sleep(0.05)
    #End_def


    async def send_memory_data(self):
        while True:
            memory_usage = self.hypervisor.memory.read()
            print(memory_usage)
            await self.send(json.dumps( memory_usage ))
            await asyncio.sleep(10)
    #End_def


    async def send_disk_data(self):
        while True:
            disk_usage = self.hypervisor.disk.read()
            print(disk_usage)
            await self.send(json.dumps( disk_usage ))
            await asyncio.sleep(10)
    #End_def

# End_class