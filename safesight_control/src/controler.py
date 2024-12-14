import numpy as np
from src.interface import Interface


class Controler:
    def __init__(self):
        self.interface = Interface()
        self.flash_active = False
        self.is_moving = False

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

    def stop(self):
        if self.is_moving:
            self.interface.stop()

    def forward(self):
        if not self.is_moving:
            self.interface.move_forward()
            self.is_moving = True

    def backward(self):
        if not self.is_moving:
            self.interface.move_backward()
            self.is_moving = True

    def left(self):
        if not self.is_moving:
            self.interface.move_left()
            self.is_moving = True

    def right(self):
        if not self.is_moving:
            self.interface.move_right()
            self.is_moving = True
