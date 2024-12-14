from src.gui import Gui
from src import interface

def main():
    gui = Gui()
    gui.setup()

if __name__ == "__main__":
    interface = interface.Interface()
    ip = "192.168.4.1"
    port = 10000

    try:
        interface.connect(ip, port)
        interface.send_message("Hello, ESP32!")
        response = interface.receive_message()
        if response:
            print(f"Response from server: {response}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        interface.disconnect()
