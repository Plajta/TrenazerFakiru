import numpy as np
import pyaudio

SAMPLE = 22050
FRAME_SIZE = 2048

def CreateStream():
    global stream
    stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE,
        input=True,
        frames_per_buffer=FRAME_SIZE)