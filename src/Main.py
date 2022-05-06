from pickle import FRAME
import Audio as A
import Video as V
import cv2

import numpy as np
import matplotlib.pyplot as plt

def Main():
    A.ViewDevices()
    A.CreateStream(6)
    video = V.init()
    while (True):
        A.Run()
        
        ret, frame = V.read(video)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        
if __name__ == "__main__":
    Main()