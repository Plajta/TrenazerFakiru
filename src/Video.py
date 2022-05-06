from types import FrameType
import cv2

def init():
    video = cv2.VideoCapture(2)
    return video

def read(video):
    ret, frame = video.read()
    return ret,frame

def display(frame):
    cv2.imshow('frame', frame)

def end(video):
    video.release()
    cv2.destroyAllWindows()