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
        A.Buffer[:-A.FRAME_SIZE] = A.Buffer[A.FRAME_SIZE:]
        A.Buffer[-A.FRAME_SIZE:] = np.fromstring(A.stream.read(A.FRAME_SIZE, exception_on_overflow = False), np.int16)

        #Run FFT
        fft = np.fft.rfft(A.Buffer * A.Hann_Win)
        freq = (np.abs(fft[A.imin:A.imax]).argmax() + A.imin) * A.FREQ_STEP

        n = A.freq_to_number(freq)
        n0 = int(round(n))

        num_frames += 1
        if num_frames >= A.FRAMES_PER_FFT:
            print("freq: {:7.2f} Hz     note: {:>3s} {:+.2f}".format(freq, A.note_name(n0), n-n0))
        
        ret, frame = V.read(video)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        
if __name__ == "__main__":
    Main()