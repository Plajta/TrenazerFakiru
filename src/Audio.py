import numpy as np
import pyaudio

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

SAMPLE = 22050
FRAME_SIZE = 2048


#Setup
PyAudioInstance = pyaudio.PyAudio()
def ViewDevices():
    info = PyAudioInstance.get_host_api_info_by_index(0)
    numdevices = info.get("deviceCount")

    for i in range(numdevices):
        if (PyAudioInstance.get_device_info_by_host_api_device_index(0, i).get("maxInputChannels")) > 0:
            print("Input Device id ", i, " - ", PyAudioInstance.get_device_info_by_host_api_device_index(0, i).get('name'))

def CreateStream(InputDeviceIndex):
    global stream
    stream = PyAudioInstance.open(format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE,
        input=True,
        frames_per_buffer=FRAME_SIZE,
        input_device_index=InputDeviceIndex
    )
    stream.start_stream()

def StopStream(): stream.stop_stream()
def DestroyStream(): stream.close()