import mediapipe as mp
import cv2
from pynput.mouse import Button, Controller
import numpy as np

#setup
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

mouse = Controller()


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
        else:
            Wrists = [[0, 0], [0, 0]]

        return cv2.flip(image, 1), results

def WristCalc(hands, im_width, im_height):
    if hands.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(hands.multi_hand_landmarks):
            Wrists[i][0] = np.round(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * im_width)
            Wrists[i][1] = np.round(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * im_height)

def DiffCalc(Diff):
    DiffX, DiffY = 0, 0
    if (Diff[1][0] != 0 and Diff[1][1] != 0) or (Diff[0][0] != 0 and Diff[0][1] != 0):
        DiffX = (Diff[0][0] + Diff[1][0]) / 2
        DiffY = (Diff[0][1] + Diff[1][1]) / 2
    return DiffX, DiffY
    
def AbsolteMouse(abs_pos):
    x = (abs_pos[0][0]+abs_pos[1][0])/2
    y = (abs_pos[0][1]+abs_pos[1][1])/2
    mouse.position = (1920-4*abs_pos[0], 2*abs_pos[1])

def RelativeMouse(DiffX, DiffY):
    mouse.move(DiffX, -DiffY)