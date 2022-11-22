import cv2
import mediapipe as mp
import time
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For static images:
IMAGE_FILES = []
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
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
        if hand_landmarks.landmark[mp_hands.HandLandmark(7).value].x * image_width < (image_width*1/3):
            print('r')
        elif hand_landmarks.landmark[mp_hands.HandLandmark(7).value].x * image_width < (image_width*2/3):
            print('m')
        elif hand_landmarks.landmark[mp_hands.HandLandmark(7).value].x * image_width < (image_width):
            print('l')
        if hand_landmarks.landmark[mp_hands.HandLandmark(7).value].y * image_height < (image_height*1/3):
            print('t')
        elif hand_landmarks.landmark[mp_hands.HandLandmark(7).value].y * image_height < (image_height*2/3):
            print('m')
        elif hand_landmarks.landmark[mp_hands.HandLandmark(7).value].y * image_height < (image_height):
            print('b')
        #print(hand_landmarks.landmark[mp_hands.HandLandmark(7).value].z * image_width)
    #   break
        # print(f'HAND NUMBER: {hand_no+1}')
        # print('-----------------------')
        # print(f'{mp_hands.HandLandmark(7).name}:') 
        # print(f'x: {hand_landmarks.landmark[mp_hands.HandLandmark(7).value].x * image_width}')
        # print(f'y: {hand_landmarks.landmark[mp_hands.HandLandmark(7).value].y * image_height}')
        # print(f'z: {hand_landmarks.landmark[mp_hands.HandLandmark(7).value].z * image_width}n')
    #time.sleep(1)
        # for i in range(20):    
        #     print(f'{mp_hands.HandLandmark(i).name}:') 
        #     print(f'x: {hand_landmarks.landmark[mp_hands.HandLandmark(i).value].x * image_width}')
        #     print(f'y: {hand_landmarks.landmark[mp_hands.HandLandmark(i).value].y * image_height}')
        #     print(f'z: {hand_landmarks.landmark[mp_hands.HandLandmark(i).value].z * image_width}n')
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()