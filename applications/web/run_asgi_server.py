'''
Communication over a port and IP address (such as http://127.0.0.1:8000) and communication over a
Unix socket (such as http://unix:/path/to/socket.sock) are two different approaches to routing requests from a
proxy server, such as Nginx, to an ASGI/HTTP server application, such as UVicorn or Gunicorn.

Communication via Unix Socket (http://unix:/path/to/socket.sock):
In this approach, the proxy server (Nginx) redirects requests through a Unix socket, which is a mechanism 
for interprocess communication on Unix systems. Communication using Unix sockets is usually faster and more secure than communication over the network due to its nature of communication between processes on the same system.
'''

import os
from uvicorn import run
from dotenv import load_dotenv
from uvicorn.protocols.http.h11_impl import H11Protocol

import django
django.setup()

from qubik.asgi import application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qubik.settings')

SOCKET_PATH = '/run/uvicorn.sock'  # Path to socket Unix

if __name__ == '__main__':
    run(
        application,      # ASGI application
        uds=SOCKET_PATH,
        http=H11Protocol
    )


'''
The following code is to use uvicorn using TCP/IP network communication instead of using 'unix sockets ' against the NGINX server. You can choose to use it by uncommenting the following lines:
'''

# import os
# from uvicorn import run
# from dotenv import load_dotenv

# import django
# django.setup()

# from qubik.asgi import application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qubik.settings')

# Global variables and paths
# load_dotenv()
# HOST = os.getenv('HOST_HYPERSOR')
# PORT = int(os.getenv('ASGI_PORT'))

# if __name__ == '__main__':
#    run(application, host=HOST, port=PORT)
