import threading, socket, json


class SocketClientController(threading.Thread):

    def __init__(self, host, port, message):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.message = message
        self.response = None
        self.error_message = None
    
    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(self.host)
            try:
                s.connect((self.host, self.port))
                s.sendall(self.message.encode())
                self.response = s.recv(1024).decode()
            except (ConnectionResetError, BrokenPipeError, OSError) as e:
                self.error_message = "Connection error: " + str(e)
    
    def get_response(self):
        return self.response
    
    def get_error_message(self):
        return self.error_message


def get_vm_resources(host, port, message):
    try:
        socket_client = SocketClientController(host, port, message)
        socket_client.start()

        # Wait for the socket thread to finish
        socket_client.join()

        # Check if there was an error message or get the response
        error_message = socket_client.get_error_message()

        if error_message:
            print(error_message)
            error = {}
            error['message'] = 'not_available'
            return error

        else:
            response_str = socket_client.get_response()
            print(response_str)
            response_str = response_str.replace("'", '"')
            try:
                response_dict = json.loads(response_str)
                return response_dict

            except json.JSONDecodeError as e:
                print("Error decoding JSON:", e)
                

    except(KeyError) as e:
        print(e)
