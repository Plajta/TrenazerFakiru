from pynput.mouse import Button, Controller
import Audio as A
import Video as V
import cv2
import sounddevice as sd
import numpy as np

mouse = Controller()
joystick = np.zeros(2)

def Main():
    global Last_loc

    video = V.init(0)

    #try:
    with sd.InputStream(channels=1, callback=A.Run, blocksize=A.WINDOW_STEP, samplerate=A.SAMPLE_FREQ):
        while True:
            ret, frame = V.read(video)
            im_height, im_width, channels = frame.shape
            if not ret: continue

            image, hands = V.HandsDetect(frame)
                
            if hands.multi_hand_landmarks:
                for i, hand_landmarks in enumerate(hands.multi_hand_landmarks):

                    V.Wrists[i][0] = np.round(hand_landmarks.landmark[V.mp_hands.HandLandmark.WRIST].x * im_width)
                    V.Wrists[i][1] = np.round(hand_landmarks.landmark[V.mp_hands.HandLandmark.WRIST].y * im_height)
            else:
                V.Wrists = [[320, 240], [320, 240]]

            
            joystick[0] = 320 - (V.Wrists[0][0] + V.Wrists[1][0]) / 2
            joystick[1] = ((V.Wrists[0][1] + V.Wrists[1][1]) / 2) - 240

            print(joystick)

            mouse.move(joystick[0], joystick[1])

            cv2.imshow('frame', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    #except Exception as e: print(str(e))
        
if __name__ == "__main__":
    Main()