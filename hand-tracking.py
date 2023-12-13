import cv2
import mediapipe as mp
import math
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Impossible de lire la vidéo")
      break

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    hand_closed = False

    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[hand_count]
        hand_count+=1
          
        wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
        middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

        thumb_cmc = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC]
        index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
        ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
        pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
        middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
        #Formule de la distance entre deux points dans un volume.

        distance_index_tip = math.sqrt((wrist.x - index_tip.x)**2 + (wrist.y - index_tip.y)**2 + (wrist.z - index_tip.z)**2)
        distance_index_cmc = math.sqrt((wrist.x - index_mcp.x)**2 + (wrist.y - index_mcp.y)**2 + (wrist.z - index_mcp.z)**2)
        distance_index = distance_index_tip-distance_index_cmc

        distance_ring_tip = math.sqrt((wrist.x - ring_tip.x)**2 + (wrist.y - ring_tip.y)**2 + (wrist.z - ring_tip.z)**2)
        distance_ring_cmc = math.sqrt((wrist.x - ring_mcp.x)**2 + (wrist.y - ring_mcp.y)**2 + (wrist.z - ring_mcp.z)**2)
        distance_ring = distance_ring_tip - distance_ring_cmc

        distance_pinky_tip = math.sqrt((wrist.x - pinky_tip.x)**2 + (wrist.y - pinky_tip.y)**2 + (wrist.z - pinky_tip.z)**2)
        distance_pinky_cmc = math.sqrt((wrist.x - pinky_mcp.x)**2 + (wrist.y - pinky_mcp.y)**2 + (wrist.z - pinky_mcp.z)**2)
        distance_pinky = distance_pinky_tip - distance_pinky_cmc

        distance_middle_tip = math.sqrt((wrist.x - middle_tip.x)**2 + (wrist.y - middle_tip.y)**2 + (wrist.z - middle_tip.z)**2)
        distance_middle_cmc = math.sqrt((wrist.x - middle_mcp.x)**2 + (wrist.y - middle_mcp.y)**2 + (wrist.z - middle_mcp.z)**2)
        distance_middle = distance_middle_tip - distance_middle_cmc


        #distance_index = math.sqrt((wrist.x - thumb_tip.x)**2 + (wrist.y - thumb_tip.y)**2 + (wrist.z - thumb_tip.z)**2) + math.sqrt((wrist.x - index_tip.x)**2 + (wrist.y - index_tip.y)**2 + (wrist.z - index_tip.z)**2)

        if distance_index < 0 and distance_ring <0 and distance_pinky<0 and  distance_middle <0 and which_hand.classification[0].index == 0:
            
            l_hand_closed = True
            pyautogui.keyDown('space')
            

        if distance_index < 0 and distance_ring <0 and distance_pinky<0 and  distance_middle <0 and which_hand.classification[0].index == 1:
            
            r_hand_closed = True
            pyautogui.press('space')     

       

        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('MediaPipe Hands', image)

    if cv2.waitKey(5) & 0xFF == 27:
      break

    print("Main fermée :", hand_closed)

cap.release()
cv2.destroyAllWindows()