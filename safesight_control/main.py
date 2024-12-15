from src.controler import Controler
from src.gui import Gui
from src import interface
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.colors import Normalize

def main():
    controler = Controler()
    gui = Gui(controler)
    gui.setup()

if __name__ == "__main__":
    main()
