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
            status = self.interface.flashon()
        else:
            status = self.interface.flashoff()

        return self.flash_active

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

    def convert_to_polar(self, measurements):
        results = []
        flag = 1
        k = 0
        for i in range(-45, 46, 2):
            az = np.radians(i)
            if flag == 1:
                for j in range(-45, 46, 2):
                    r = measurements[k] / 5800
                    ver = np.radians(j)
                    results.append(
                        (
                            r * np.cos(ver) * np.cos(az),
                            r * np.cos(ver) * np.sin(az),
                            r * np.sin(ver),
                        )
                    )
                    k += 1
            else:
                for j in range(45, -46, -2):
                    r = measurements[k] / 5800
                    ver = np.radians(j)
                    results.append(
                        (
                            r * np.cos(ver) * np.cos(az),
                            r * np.cos(ver) * np.sin(az),
                            r * np.sin(ver),
                        )
                    )
                    k += 1
            flag *= -1
        return results

    def run_audio_scan(self): ...
