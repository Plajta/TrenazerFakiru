import mediapipe as mp
import cv2
#from pynput.mouse import Button, Controller
import numpy as np
import pyautogui

#setup
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

#mouse = Controller()
Default_X = 320
Default_Y = 240
joystick = np.zeros(2)

Wrists = [[0, 0], [0, 0]]

def init(count):
    video = cv2.VideoCapture(count)
    return video

def read(video):
    ret, frame = video.read()
    return ret,frame

def display(frame):
    cv2.imshow('frame', frame)

def end(video):
    video.release()
    cv2.destroyAllWindows()

def HandsDetect(image):
    with mp_hands.Hands(model_complexity = 0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        
        #print(results.multi_handedness)
        #print(results.multi_hand_landmarks)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS, 
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        #cv2.imshow("frame", image)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    exit()   

        return cv2.flip(image, 1), results

def Main():
    Wrists = [[0, 0], [0, 0]]
    video = init(2)
    while True:
        ret, frame = video.read()
        im_height, im_width, channels = frame.shape
        if not ret: continue

        image, hands = HandsDetect(frame)
            
        if hands.multi_hand_landmarks:
            for i, hand_landmarks in enumerate(hands.multi_hand_landmarks):

                Wrists[i][0] = np.round(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * im_width)
                Wrists[i][1] = np.round(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * im_height)
        else:
            Wrists = [[320, 240], [320, 240]]

        
        joystick[0] = (Default_X - (Wrists[0][0] + Wrists[1][0]) / 2)/3
        joystick[1] = (((Wrists[0][1] + Wrists[1][1]) / 2) - Default_Y)/3

        #targetX = joystick[0]
        #targetY = joystick[1]
        #print(joystick[0])
        #print(joystick[1])

        if np.abs(joystick[0]) < 5: joystick[0] = 0
        elif np.abs(joystick[1]) < 5: joystick[1] = 0

        #print(joystick)

        pyautogui.move(joystick[0],joystick[1])
        #pyautogui.move(joystick[0],joystick[1], 0.1, pyautogui.easeInOutSine)

        cv2.imshow('frame', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    Main()