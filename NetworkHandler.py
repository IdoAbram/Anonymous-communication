import socket

class NetworkHandler:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def listen(self):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.ip, self.port))
            server_socket.listen(1)
            print(f"Listening on {self.ip}:{self.port}...")
            while True:
                client_socket, client_address = server_socket.accept()
                print(f"Connection from {client_address}")
                data = client_socket.recv(2048)
                if data:
                    self.handle_received_data(data.decode())
                client_socket.close()
        except Exception as e:
            print(f"An error occurred: {e}")

    def send_data(self, ip, port, message):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip, port))
            client_socket.send(message.encode())
            client_socket.close()
        except Exception as e:
            print(f"An error occurred: {e}")

    def handle_received_data(self, data):
        # Override this method in a subclass to handle received data
        pass