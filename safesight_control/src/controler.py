import numpy as np
from src.interface import Interface

class Controler:
    def __init__(self):
        self.interface = Interface()
        self.flash_active = False
        self.is_moving = False
        self.movement_enabled = True
        self.scan_canceled = False

    def get_camera_view(self):
        data = self.interface.get_image()
        if not data:
            return np.zeros((480, 640, 3), dtype="float32").flatten() / 255

        img = np.array(data).astype("float32")
        return img.flatten() / 255

    def toggle_flash(self):
        status = False
      
        self.flash_active = not self.flash_active

        if self.flash_active:
            self.interface.flashon()
        else:
            self.interface.flashoff()

        return self.flash_active
    
    def convert_to_polar(self, measurements):
        horiz_min = measurements[0]
        horiz_max = measurements[1]
        vertic_min = measurements[2]
        vertic_max = measurements[3]
        print(len(measurements))
        self.interface.disconnect()
        results = []
        flag = 1
        k = 4
        for i in range(horiz_min, horiz_max, 2):
            az = math.radians(i)
            if flag == 1:
                for j in range(vertic_min, vertic_max + 1, 2):
                    r = measurements[k] / 5800 + 0.055
                    ver = math.radians(j)
                    results.append((r * math.cos(ver) * math.cos(az), r * math.cos(ver) * math.sin(az),r * math.sin(ver)))
                    k += 1
            else:
                for j in range(vertic_max, vertic_min - 1, -2):
                    r = measurements[k] / 5800 + 0.055
                    ver = math.radians(j)
                    results.append((r * math.cos(ver) * math.cos(az), r * math.cos(ver) * math.sin(az),r * math.sin(ver)))
                    k += 1
            flag *= -1
        return results
    
    def run_audio_scan(self):
        signal = self.interface.get_audio_measurements()
        fs = signal[0]
        T = signal[1]
        t = np.linspace(0, T, int(fs * T), endpoint=False)  
        
        fft_result = np.fft.fft(signal[2:]) 
        frequencies = np.fft.fftfreq(len(t), d=1/fs)
        return fft_result[:len(frequencies) // 2], frequencies[:len(frequencies) // 2]  

    def stop(self):
        if self.is_moving and self.movement_enabled:
            self.interface.stop()

    def forward(self):
        if not self.is_moving and self.movement_enabled:
            self.interface.move_forward()
            self.is_moving = True

    def backward(self):
        if not self.is_moving and self.movement_enabled:
            self.interface.move_backward()
            self.is_moving = True

    def left(self):
        if not self.is_moving and self.movement_enabled:
            self.interface.move_left()
            self.is_moving = True

    def right(self):
        if not self.is_moving and self.movement_enabled:
            self.interface.move_right()
            self.is_moving = True

    def run_3d_scan(self):
        return self.convert_to_polar(self.interface.get_point_cloud())