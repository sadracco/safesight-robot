import http
import http.client
import socket
import sys
from io import BytesIO
import requests
from PIL import Image

class Interface:
    def __init__(self):
        self.master_ip = "192.168.4.1"
        self.master_port = 10000
        self.camera_ip = "192.168.4.2"

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(5)
        try:
            self.client_socket.connect((self.master_ip, self.master_port))
        except Exception as e:
            print(f"Unable to connect to {self.master_ip}")
            print(e)
            sys.exit(0)

    def camera_request(self, endpoint):
        try:
            return requests.get(f"http://{self.camera_ip}/{endpoint}", timeout=(3, 5))
        except:
            return False

    def flashon(self):
        return self.camera_request("flashon")

    def flashoff(self):
        return self.camera_request("flashoff")

    def get_image(self):
        response = self.camera_request("image")

        if not response:
            return False
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))

        return False

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

    def move_forward(self):
        self.send_message("forward")

    def move_backward(self):
        self.send_message("backward")

    def stop(self):
        self.send_message("stop")

    def move_left(self):
        self.send_message("left")

    def move_right(self):
        self.send_message("right")

    def get_point_cloud(self):
        measurements = []
        self.send_message("scandistance")
        while True:
            data = self.receive_message()
            data = data.split(",")
            for p in data:
                if p == "\n":
                    return measurements
                if p != "":
                    measurements.append(int(p))
    
    def get_audio_measurements(self):
        measurements = []
        self.send_message("scanaudio")
        while True:
            data = self.receive_message()
            data = data.split(",")
            for p in data:
                if p == "\n":
                    return measurements
                if p != "":
                    measurements.append(int(p))
                    
    def __del__(self):
        self.client_socket.close()