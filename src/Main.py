from pickle import FRAME
import Audio as A
import Video as V

import numpy as np
import matplotlib.pyplot as plt

def Main():
    A.ViewDevices()

    A.CreateStream(8)
    while A.stream.is_active():
        A.Run()
        
    

if __name__ == "__main__":
    Main()