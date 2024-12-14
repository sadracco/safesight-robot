import threading

import dearpygui.dearpygui as dpg
import matplotlib.pyplot as plt
from src.controler import Controler


class Gui:
    def __init__(self, controler: Controler):
        self.controler = controler

    def setup(self):
        dpg.create_context()
        dpg.create_viewport(title="Safesight Control")
        dpg.setup_dearpygui()

        # movement control
        with dpg.window(label="Movement control", autosize=True, no_close=True):
            dpg.add_text("Use the keyboard to move the robot")
            dpg.add_text("W to move forwards", tag="movement_w")
            dpg.add_text("S to move backwards", tag="movement_s")
            dpg.add_text("A to turn left", tag="movement_a")
            dpg.add_text("D to turn right", tag="movement_d")

        # camera stream
        with dpg.texture_registry():
            dpg.add_raw_texture(
                width=640,
                height=480,
                default_value=self.controler.get_camera_view(),
                format=dpg.mvFormat_Float_rgb,
                tag="camera_view",
            )

        with dpg.window(label="Camera image", autosize=True, no_close=True):
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Toggle flash",
                    callback=self.camera_flash_toggle_callback,
                    tag="camera_flash_toggle",
                )

                dpg.add_text(
                    "OFF", color=(255, 0, 0, 255), tag="camera_flash_indicator"
                )
            dpg.add_image("camera_view")

        # sensing tasks
        with dpg.window(label="Sensing tasks", autosize=True, no_close=True):
            dpg.add_button(
                label="Toggle flash",
                callback=self.camera_flash_toggle_callback,
                tag="camera_flash_toggle",
            )

        # global keypresses
        with dpg.handler_registry():
            dpg.add_key_down_handler(
                dpg.mvKey_W, callback=self.movement_control_callback, user_data="w"
            )
            dpg.add_key_release_handler(
                dpg.mvKey_W, callback=self.movement_control_reset_callback
            )
            dpg.add_key_down_handler(
                dpg.mvKey_A, callback=self.movement_control_callback, user_data="a"
            )
            dpg.add_key_release_handler(
                dpg.mvKey_A, callback=self.movement_control_reset_callback
            )
            dpg.add_key_down_handler(
                dpg.mvKey_S, callback=self.movement_control_callback, user_data="s"
            )
            dpg.add_key_release_handler(
                dpg.mvKey_S, callback=self.movement_control_reset_callback
            )
            dpg.add_key_down_handler(
                dpg.mvKey_D, callback=self.movement_control_callback, user_data="d"
            )
            dpg.add_key_release_handler(
                dpg.mvKey_D, callback=self.movement_control_reset_callback
            )

        thread = threading.Thread(target=self.camera_update_thread)
        thread.daemon = True
        thread.start()

        dpg.show_viewport(maximized=True)
        dpg.start_dearpygui()
        dpg.destroy_context()

    def movement_control_callback(self, sender, app_data, user_data):
        if app_data[1] != 0:
            return

        match user_data:
            case "w":
                self.controler.forward()
                dpg.configure_item("movement_w", color=(0, 255, 255, 255))
            case "a":
                self.controler.left()
                dpg.configure_item("movement_a", color=(0, 255, 255, 255))
            case "s":
                self.controler.backward()
                dpg.configure_item("movement_s", color=(0, 255, 255, 255))
            case "d":
                self.controler.right()
                dpg.configure_item("movement_d", color=(0, 255, 255, 255))

    def movement_control_reset_callback(self, sender, app_data, user_data):
        self.controler.stop()
        dpg.configure_item("movement_w", color=(-255, 0, 0, 255))
        dpg.configure_item("movement_a", color=(-255, 0, 0, 255))
        dpg.configure_item("movement_s", color=(-255, 0, 0, 255))
        dpg.configure_item("movement_d", color=(-255, 0, 0, 255))

    def camera_flash_toggle_callback(self, sender, app_data, user_data):
        if self.controler.toggle_flash():
            dpg.configure_item("camera_flash_indicator", color=(0, 255, 0, 255))
        else:
            dpg.configure_item("camera_flash_indicator", color=(255, 0, 0, 255))

    def camera_update_thread(self):
        while True:
            dpg.set_value("camera_view", self.controler.get_camera_view())
