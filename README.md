# TrenazerFakiru
Trenažer Fakírů (Fakir trainer) is a special software used to train Fakirs by controlling a whole computer by flute (we won an AimtecHackathon 2022 in Pilsen with this one)
This code is divided into audio (used Fast Fourier transform with sounddevice library) and video part (mediapipe with Wrist acceleration detection)

> ## Known Bugs
> 1. Too slow (maybe change algorithm and minimize usage of neural networks)
> 2. Mouse control is hard and not too much user friendly
> 3. You literally need to spam the tone to actually get it invoked on computer
> 4. Huge latency in Button control (same as point 3.)

Used libraries: `mediapipe`, `pyaudio`, `sounddevice`, `scipy`, `pynput`, `pyautogui`, `cv2`, `numpy`
