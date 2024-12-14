import socket

import requests


class Interface:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.master_ip = "192.168.4.1"
        self.master_port = 10000
        self.camera_ip = "192.168.4.2"

    def camera_url(self, endpoint):
        return f"http://{self.master_ip}/{endpoint}"

    def flashon(self):
        requests.get(self.camera_url("/flashon"))

    def flashoff(self):
        requests.get(self.camera_url("/flashoff"))

    def connect(self, ip, port):
        self.client_socket.connect((ip, port))

    def disconnect(self):
        self.client_socket.close()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_message(self, message):
        try:
            self.client_socket.sendall(message.encode("utf-8"))
        except socket.error as e:
            print(f"Error sending message: {e}")

    def receive_message(self, buffer_size=1024):
        try:
            response = self.client_socket.recv(buffer_size)
            message = response.decode("utf-8")
            return message
        except socket.error as e:
            return None
