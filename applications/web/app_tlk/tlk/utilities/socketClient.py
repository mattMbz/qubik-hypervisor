import threading, socket
from time import sleep


class SocketClientController(threading.Thread):

    def __init__(self, host, port, time, message):
        threading.Thread.__init__(self)
        self.stop = False
        self.host = host
        self.port = port
        self.message = message
        self.time = time
    #End_def
    
    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.host, self.port))

                while not self.stop:
                    sleep(self.time)
                    s.sendall(self.message.encode())
                    data = s.recv(1024)
                    print(data.decode())

            except (ConnectionResetError, BrokenPipeError) as e:
                print("Connection error: ", e)
    #End_def

    def stop_socket_client(self):
        self.stop = True
        print("STOP")
    #End_def

#End_class



HOST = "192.168.122.21"  # Virtual Machine IP
PORT = 8503              # Port to send data
TIME = 1.2
MESSAGE = 'cpu'

cpu_socket=SocketClientController(HOST, PORT, TIME, MESSAGE)
cpu_socket.start()

# memory_socket=SocketClientController(HOST, PORT, 'memory')
# memory_socket.start()

#disk_socket=SocketClientController(HOST, PORT, 'disk')
#disk_socket.start()