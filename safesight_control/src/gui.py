<<<<<<< Updated upstream
=======
import threading
>>>>>>> Stashed changes
import dearpygui.dearpygui as dpg

from src.controler import Controler


class Gui:
    def __init__(self, controler: Controler = None):
        self.controler = controler

    def setup(self):
        dpg.create_context()
        dpg.create_viewport(title="Safesight Control")
        dpg.setup_dearpygui()

<<<<<<< Updated upstream
        # movement control
        with dpg.window(label="Movement control", autosize=True):
=======
        with dpg.window(label="Movement control", autosize=True, no_close=True):
>>>>>>> Stashed changes
            dpg.add_text("Use the keyboard to move the robot")
            dpg.add_text("W to move forwards", tag="text_w")
            dpg.add_text("S to move backwards", tag="text_s")
            dpg.add_text("A to turn left", tag="text_a")
            dpg.add_text("D to turn right", tag="text_d")

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

        dpg.show_viewport(maximized=True)
        dpg.start_dearpygui()
        dpg.destroy_context()

    def movement_control_callback(self, sender, app_data, user_data):
        if app_data[1] != 0:
            return

        match user_data:
            case "w":
                dpg.configure_item("text_w", color=(0, 255, 255, 255))
            case "a":
                dpg.configure_item("text_a", color=(0, 255, 255, 255))
            case "s":
                dpg.configure_item("text_s", color=(0, 255, 255, 255))
            case "d":
                dpg.configure_item("text_d", color=(0, 255, 255, 255))

    def movement_control_reset_callback(self, sender, app_data, user_data):
        dpg.configure_item("text_w", color=(-255, 0, 0, 255))
        dpg.configure_item("text_a", color=(-255, 0, 0, 255))
        dpg.configure_item("text_s", color=(-255, 0, 0, 255))
        dpg.configure_item("text_d", color=(-255, 0, 0, 255))
