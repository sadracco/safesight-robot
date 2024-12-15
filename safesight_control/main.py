from src.controler import Controler
from src.gui import Gui
from src import interface
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.colors import Normalize
import time

def main():
    C = Controler()
    C.forward()
    time.sleep(10)
    C.stop()

if __name__ == "__main__":
    main()
