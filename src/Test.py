import Audio as A
import Video as V
import cv2

import numpy as np

def Main():
    A.ViewDevices()
    A.CreateStream(8)
    video = V.init()
    while True:
        #TODO: Pomoc!
        
        ret, frame = V.read(video)
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

if __name__ == "__main__":
    Main()
