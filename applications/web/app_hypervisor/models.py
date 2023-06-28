# from django.db import models

import uuid

virtual_machines = [
    {
     'name':'nodejs-app', 
     'id': str(uuid.uuid4()).split('-')[4],
     'status': 'ON',
     'appName':'siu guaraní 3.17',
     'version':'3.17',
     'vcpu':'4',
     'vram':'4',
     'vdisk':'10',
    },
    {
     'name':'Debian10-vm', 
     'id': str(uuid.uuid4()).split('-')[4],
     'status':'ON',
    },
    {
        'name':'flaskapi',  
        'id': str(uuid.uuid4()).split('-')[4],
        'status': 'ON'
    },
    {'name':'vm-universidad', 'id': str(uuid.uuid4()).split('-')[4], 'status': 'ON'},
    {'name':'vm-universidad', 'id': str(uuid.uuid4()).split('-')[4], 'status': 'ON'},
    {'name':'vm-universidad', 'id': str(uuid.uuid4()).split('-')[4], 'status': 'ON'},
    {'name':'vm-universidad', 'id': str(uuid.uuid4()).split('-')[4], 'status': 'ON'}
]
