import numpy as np
import pyaudio

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

SAMPLE = 22050
FRAME_SIZE = 2048
FRAMES_PER_FFT = 16
SAMPLES_PER_FFT = FRAME_SIZE * FRAMES_PER_FFT
FREQ_STEP = float(SAMPLE) / SAMPLES_PER_FFT
NOTE_MIN = 60 #C4
NOTE_MAX = 69 #A4

#Setup
PyAudioInstance = pyaudio.PyAudio()
Buffer = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
#Hanning Window Function
Hann_Win = 0.5 * (1 - np.cos(np.linspace(0, 2 * np.pi, SAMPLES_PER_FFT, False)))

#Conversion
def freq_to_number(f): return 69 + 12 * np.log2(f / 440.0)
def number_to_freq(n): return 440 * 2.0 ** ((n - 69) / 12.0)
def note_name(n): return NOTES[n % 12] + str(n / 12 - 1)
def note_to_fftbin(n): return number_to_freq(n) / FREQ_STEP

imin = max(0, int(np.floor(note_to_fftbin(NOTE_MIN - 1))))
imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX + 1))))

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