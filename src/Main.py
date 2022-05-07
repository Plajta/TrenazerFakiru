import Audio as A
import Video as V
import cv2
import sounddevice as sd

import numpy as np

Last_loc = np.zeros((2, 2))

def Main():
    global Last_loc, DiffX, DiffY

    video = V.init(0)

    try:
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


                Current_loc = np.array(V.Wrists)
                Diff = np.subtract(Last_loc, Current_loc)
                #print(Diff)
                
                Last_loc = Current_loc

                if (Diff[1][0] != 0 and Diff[1][1] != 0) or (Diff[0][0] != 0 and Diff[0][1] != 0):
                    DiffX = (Diff[0][0] + Diff[1][0]) / 2
                    DiffY = (Diff[0][1] + Diff[1][1]) / 2
                else:
                    Diff[0][0] = DiffX
                    Diff[0][1] = DiffY

                print(DiffX, DiffY)

                cv2.imshow('frame', image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    except Exception as e: print(str(e))
        
if __name__ == "__main__":
    Main()