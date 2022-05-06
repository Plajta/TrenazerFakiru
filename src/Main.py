import Audio as A
import Video as V
import cv2
import sounddevice as sd

import numpy as np
import matplotlib.pyplot as plt

def Main():
    video = V.init(0)

    try:
        with sd.InputStream(channels=1, callback=A.Run, blocksize=A.WINDOW_STEP, samplerate=A.SAMPLE_FREQ):
            while (True):
                ret, frame = V.read(video)
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    except Exception as e: print(str(e))
        
if __name__ == "__main__":
    Main()