import numpy as np
from src.interface import Interface


class Controler:
    def __init__(self):
        self.interface = Interface()
        self.flash_active = False

    def get_camera_view(self):
        return np.ones((480, 680, 3), dtype=np.float32).flatten() / 255

    def toggle_flash(self):
        self.flash_active = not self.flash_active

        if self.flash_active:
            self.interface.flashon()
        else:
            self.interface.flashoff()

        return self.flash_active
