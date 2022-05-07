from cgi import MiniFieldStorage
import mediapipe as mp
import cv2
from pynput.mouse import Button, Controller

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

def AbsolteMouse(abs_pos):
    mouse.position = (1920-4*abs_pos[0], 2*abs_pos[1])