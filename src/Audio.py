import sounddevice as sd
import numpy as np
import scipy.fftpack
from pynput.keyboard import Key, Controller
import os

# General settings
SAMPLE_FREQ = 44100 # sample frequency in Hz
WINDOW_SIZE = 44100 # window size of the DFT in samples
WINDOW_STEP = 21050 # step size of window
WINDOW_T_LEN = WINDOW_SIZE / SAMPLE_FREQ # length of the window in seconds
SAMPLE_T_LENGTH = 1 / SAMPLE_FREQ # length between two samples in seconds
windowSamples = [0 for _ in range(WINDOW_SIZE)]
keyboard = Controller()

oskstate = False

# This function finds the closest note for a given pitch
# Returns: note (e.g. A4, G#3, ..), pitch of the tone
CONCERT_PITCH = 440
ALL_NOTES = ["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]
def find_closest_note(pitch):
  i = int(np.round(np.log2(pitch/CONCERT_PITCH)*12))
  closest_note = ALL_NOTES[i%12] + str(4 + (i + 9) // 12)
  closest_pitch = CONCERT_PITCH*2**(i/12)
  return closest_note, closest_pitch

# The sounddecive callback function
# Provides us with new data once WINDOW_STEP samples have been fetched
def Run(indata, frames, time, status):
  global windowSamples
  if status:
    print(status)
  if any(indata):
    windowSamples = np.concatenate((windowSamples,indata[:, 0])) # append new samples
    windowSamples = windowSamples[len(indata[:, 0]):] # remove old samples
    magnitudeSpec = abs( scipy.fftpack.fft(windowSamples)[:len(windowSamples)//2] )

    for i in range(int(62/(SAMPLE_FREQ/WINDOW_SIZE))):
      magnitudeSpec[i] = 0 #suppress mains hum

    maxInd = np.argmax(magnitudeSpec)
    maxFreq = maxInd * (SAMPLE_FREQ/WINDOW_SIZE)
    closestNote, closestPitch = find_closest_note(maxFreq)

    print(f"Closest note: {closestNote} {maxFreq:.1f}/{closestPitch:.1f}")
    if closestNote == "C5":
      keyboard.press('D')
    elif closestNote == "D5":
      keyboard.press('S')
    elif closestNote == "E5":
      keyboard.press('A')
    elif closestNote == "F5":
      keyboard.press('W')
    elif closestNote == "G5":
      keyboard.press(Key.space)
    elif closestNote == "H5":
      if oskstate:
        os.system("gsettings set org.gnome.desktop.a11y.applications screen-keyboard-enabled true")
        
      else:
        os.system("gsettings set org.gnome.desktop.a11y.applications screen-keyboard-enabled false")
    else:
      keyboard.release('D')
      keyboard.release('S')
      keyboard.release('A')
      keyboard.release('W')
      keyboard.release(Key.space)
  else:
    #print('no input')
    pass
  
  #print(f"Closest note: {closestNote} {maxFreq:.1f}/{closestPitch:.1f}")