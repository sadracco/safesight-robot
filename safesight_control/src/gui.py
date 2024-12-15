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
        with dpg.window(
            label="Movement control", autosize=True, no_close=True, pos=(10, 20)
        ):
            dpg.add_text(
                "Robot movement enabled", color=(0, 255, 0, 255), tag="movement_enabled"
            )
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

        with dpg.window(
            label="Camera image", autosize=True, no_close=True, pos=(300, 20)
        ):
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
        with dpg.window(
            label="Scanning tasks", autosize=True, no_close=True, pos=(1000, 20)
        ):
            dpg.add_separator(label="Available scans")
            dpg.add_button(
                label="Run 3D Scan",
                callback=self.scan_3d_activate_callback,
                tag="scan_3d_button",
            )
            dpg.add_button(
                label="Run audio Scan",
                callback=self.scan_audio_activate_callback,
                tag="scan_audio_button",
            )
            dpg.add_separator(label="Scanning status")
            dpg.add_text("No scans running, robot movement enabled", tag="scan_status")
            dpg.add_loading_indicator(show=False, tag="scan_indicator")

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
            dpg.set_value("camera_flash_indicator", "ON")
        else:
            dpg.configure_item("camera_flash_indicator", color=(255, 0, 0, 255))
            dpg.set_value("camera_flash_indicator", "OFF")

    def scan_3d_activate_callback(self, sender, app_data, user_data):
        dpg.set_value("scan_status", "3D scan in progress")
        dpg.configure_item("scan_indicator", show=True)
        dpg.configure_item("movement_enabled", color=(255, 0, 0, 255))
        dpg.set_value("movement_enabled", "Robot movement disabled")
        dpg.configure_item("scan_3d_button", show=False)
        dpg.configure_item("scan_audio_button", show=False)

        self.controler.run_3d_scan()

        dpg.set_value("scan_status", "3D scan finished")
        dpg.configure_item("scan_indicator", show=False)
        dpg.configure_item("movement_enabled", color=(0, 255, 0, 255))
        dpg.set_value("movement_enabled", "Robot movement enabled")
        dpg.configure_item("scan_3d_button", show=True)
        dpg.configure_item("scan_audio_button", show=True)

    def scan_audio_activate_callback(self, sender, app_data, user_data):
        dpg.set_value("scan_status", "Audio scan in progress")
        dpg.configure_item("scan_indicator", show=True)
        dpg.configure_item("movement_enabled", color=(255, 0, 0, 255))
        dpg.set_value("movement_enabled", "Robot movement disabled")
        dpg.configure_item("scan_3d_button", show=False)
        dpg.configure_item("scan_audio_button", show=False)

        self.controler.run_audio_scan()

        dpg.set_value("scan_status", "Audio scan finished")
        dpg.configure_item("scan_indicator", show=False)
        dpg.configure_item("movement_enabled", color=(0, 255, 0, 255))
        dpg.set_value("movement_enabled", "Robot movement enabled")
        dpg.configure_item("scan_3d_button", show=True)
        dpg.configure_item("scan_audio_button", show=True)

    def camera_update_thread(self):
        while True:
            dpg.set_value("camera_view", self.controler.get_camera_view())
