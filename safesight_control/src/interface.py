import socket
import math

class Interface:
    def __init__(self, ip = '192.168.1.1', port = 10000):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port

    def connect(self):
        self.client_socket.connect((self.ip, self.port))

    def disconnect(self):
        self.client_socket.close()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_message(self, message):
        try:
            self.client_socket.sendall(message.encode('utf-8'))
        except socket.error as e:
            print(f"Error sending message: {e}")

    def receive_message(self, buffer_size=1024):
        try:
            response = self.client_socket.recv(buffer_size)
            message = response.decode('utf-8')
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

    @staticmethod
    def convert_to_polar(measurements):
        results = []
        flag = 1
        k = 0
        for i in range(-45, 46, 2):
            az = math.radians(i)
            if flag == 1:
                for j in range(-45, 46, 2):
                    r = measurements[k] / 5800
                    ver = math.radians(j)
                    results.append((r * math.cos(ver) * math.cos(az), r * math.cos(ver) * math.sin(az),r * math.sin(ver)))
                    k += 1
            else:
                for j in range(45, -46, -2):
                    r = measurements[k] / 5800
                    ver = math.radians(j)
                    results.append((r * math.cos(ver) * math.cos(az), r * math.cos(ver) * math.sin(az),r * math.sin(ver)))
                    k += 1
            flag *= -1
        return results

    def get_point_cloud(self):
        measurements = []
        self.send_message("cloud")
        while True:
            data = self.receive_message()
            data = data.split(",")
            for p in data:
                if p == "\n":
                    print(measurements)
                    print(len(measurements))
                    return self.convert_to_polar(measurements)
                if p != "":
                    measurements.append(int(p))

        

        


    

