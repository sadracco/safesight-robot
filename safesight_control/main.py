from src.controler import Controler
from src.gui import Gui
from src import interface

def main():
    controler = Controler()
    gui = Gui(controler)
    gui.setup()

if __name__ == "__main__":
    main()
