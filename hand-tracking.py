from matplotlib import pyplot as plt
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import cv2

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

capture = cv2.VideoCapture(0)

frameWidth = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
frameHeight = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

drawingModule = mp.solutions.drawing_utils
handsModule = mp.solutions.hands

while (True):
    ret, frame = capture.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    results =  mp_hands.Hands().process(frame)
    
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame,hand_landmarks,connections=mp_hands.HAND_CONNECTIONS)


    cv2.imshow('Hand Tracking', frame)
    if cv2.waitKey(1) == 27:
        break

capture.release()
cv2.destroyAllWindows()


