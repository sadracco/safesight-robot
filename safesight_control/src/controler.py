import numpy as np
from src.interface import Interface


class Controler:
    def __init__(self):
        self.interface = Interface()
        self.flash_active = False

    def get_camera_view(self):
        data = self.interface.get_image()
        if not data:
            return np.zeros((480, 640, 3), dtype="float32").flatten() / 255

        img = np.array(data).astype("float32")
        return img.flatten() / 255

    def toggle_flash(self):
        self.flash_active = not self.flash_active

        if self.flash_active:
            self.interface.flashon()
        else:
            self.interface.flashoff()

        return self.flash_active
