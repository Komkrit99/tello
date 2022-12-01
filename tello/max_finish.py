import cv2
import mediapipe as mp
import time
import pandas as pd
import pickle
import numpy as np
from djitellopy import Tello
import threading
maxi = []
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))
state = 0
lr = 0
fb = 0
ud = 0
ya = 0
# tello = Tello()
# tello.connect()
# tello.streamon()

def control_drone():
  print('start')
  global lr,fb,ud,ya,state
  while True:
    # tello.send_rc_control(lr,fb,ud,ya)
    if state == 1:
        print(lr,fb,ud,ya)
    time.sleep(0.3)
# For static images:
IMAGE_FILES = []
def most_frequent(List):
    counter = 0
    num = List[0]
     
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
 
    return num
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5) as hands:
  for idx, file in enumerate(IMAGE_FILES):
    # Read an image, flip it around y-axis for correct handedness output (see
    # above).
    image = cv2.flip(cv2.imread(file), 1)
    # Convert the BGR image to RGB before processing.
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Print handedness and draw hand landmarks on the image.
    print('Handedness:', results.multi_handedness)
    if not results.multi_hand_landmarks:
      continue
    image_height, image_width, _ = image.shape
    annotated_image = image.copy()
    for hand_landmarks in results.multi_hand_landmarks:
      print('hand_landmarks:', hand_landmarks)
      print(
          f'Index finger tip coordinates: (',
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
      )
      mp_drawing.draw_landmarks(
          annotated_image,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style())
    cv2.imwrite(
        '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
    # Draw hand world landmarks.
    if not results.multi_hand_world_landmarks:
      continue
    for hand_world_landmarks in results.multi_hand_world_landmarks:
      mp_drawing.plot_landmarks(
        hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)

# For webcam input:
cap = cv2.VideoCapture(0)
threading.Thread(target=control_drone).start()
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    image_width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
    image_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue
    value  = []
    if len(maxi) >= 5:
        maxi.pop(0)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_no,hand_landmarks in enumerate(results.multi_hand_landmarks):
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
        for a in range(21):
            value.append(hand_landmarks.landmark[mp_hands.HandLandmark(a).value].x)
            value.append(hand_landmarks.landmark[mp_hands.HandLandmark(a).value].y)
            value.append(hand_landmarks.landmark[mp_hands.HandLandmark(a).value].z)
        if len(value) == 63:
            if np.max(loaded_model.predict_proba([value]))> 0.8:
                #print(loaded_model.predict([value]),np.max(loaded_model.predict_proba([value])))
            # print(value,len(value))
                maxi.append(loaded_model.predict([value])[0])
                value  = []
    else:
        maxi.append('none')
    #print(maxi)
    #print(most_frequent(maxi))
    if state == 0 and most_frequent(maxi) == 'tf':
        state = 1
        print('take off and change state')
        # tello.takeoff() 
    if state == 1 and most_frequent(maxi) == 'ld':
        state = 0
        print('land and change state')
        # tello.land()
    if state == 1 and most_frequent(maxi) == 'fb':
        if hand_landmarks.landmark[mp_hands.HandLandmark(7).value].x * image_width < (image_width*1/3):
            lr = -20
        elif hand_landmarks.landmark[mp_hands.HandLandmark(7).value].x * image_width < (image_width*2/3):
            lr = 0
        elif hand_landmarks.landmark[mp_hands.HandLandmark(7).value].x * image_width < (image_width):
            lr = 20
        if hand_landmarks.landmark[mp_hands.HandLandmark(7).value].y * image_height < (image_height*1/3):
            fb = 20
        elif hand_landmarks.landmark[mp_hands.HandLandmark(7).value].y * image_height < (image_height*2/3):
            fb = 0
        elif hand_landmarks.landmark[mp_hands.HandLandmark(7).value].y * image_height < (image_height):
            fb = -20
        print(most_frequent(maxi))
    if state == 1 and most_frequent(maxi) == 'ud':
        if hand_landmarks.landmark[mp_hands.HandLandmark(7).value].x * image_width < (image_width*1/3):
            lr = -20
        elif hand_landmarks.landmark[mp_hands.HandLandmark(7).value].x * image_width < (image_width*2/3):
            lr = 0
        elif hand_landmarks.landmark[mp_hands.HandLandmark(7).value].x * image_width < (image_width):
            lr = 20
        if hand_landmarks.landmark[mp_hands.HandLandmark(7).value].y * image_height < (image_height*1/3):
            ud = 20
        elif hand_landmarks.landmark[mp_hands.HandLandmark(7).value].y * image_height < (image_height*2/3):
            ud = 0
        elif hand_landmarks.landmark[mp_hands.HandLandmark(7).value].y * image_height < (image_height):
            ud = -20
        print(most_frequent(maxi))
    if state == 1 and most_frequent(maxi) == 'ro':
        if hand_landmarks.landmark[mp_hands.HandLandmark(7).value].x * image_width < (image_width*1/3):
            lr = -20
        elif hand_landmarks.landmark[mp_hands.HandLandmark(7).value].x * image_width < (image_width*2/3):
            lr = 0
        elif hand_landmarks.landmark[mp_hands.HandLandmark(7).value].x * image_width < (image_width):
            lr = 20
        if hand_landmarks.landmark[mp_hands.HandLandmark(7).value].y * image_height < (image_height*1/3):
            ya = 20
        elif hand_landmarks.landmark[mp_hands.HandLandmark(7).value].y * image_height < (image_height*2/3):
            ya = 0
        elif hand_landmarks.landmark[mp_hands.HandLandmark(7).value].y * image_height < (image_height):
            ya = -20
        print(most_frequent(maxi))
    if state == 1 and most_frequent(maxi) == 'st':
        print(most_frequent(maxi))
        lr = 0
        fb = 0
        ud = 0
        y = 0
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break

#print(data)
cap.release()

# tello.streamoff()