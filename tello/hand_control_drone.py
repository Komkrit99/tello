import logging
import socket
import sys
import time
import cv2
import mediapipe as mp
import threading
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
global lr,fb,ud,y,a
lr = '0'
fb = '0'
ud = '0'
y = '0'
a = 0

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


class DroneManager(object):
    def __init__(self, host_ip='192.168.10.2', host_port=8889,
                 drone_ip='192.168.10.1', drone_port=8889):
        self.host_ip = host_ip
        self.host_port = host_port
        self.drone_ip = drone_ip
        self.drone_port = drone_port
        self.drone_address = (drone_ip, drone_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host_ip, self.host_port))
        self.socket.sendto(b'command', self.drone_address)
        self.socket.sendto(b'streamon', self.drone_address)

    def __dell__(self):
        self.stop()

    def stop(self):
        self.socket.close()

    def send_command(self, command):
        logger.info({'action': 'send_command', 'command': command})
        self.socket.sendto(command.encode('utf-8'), self.drone_address)

    def takeoff(self):
        self.send_command('takeoff')

    def land(self):
        self.send_command('land')
def drone_command():
    global lr,fb,ud,y,a
    while a == 0:
        print(f'rc {lr} {fb} {ud} {y}')
        drone_manager.send_command(f'rc {lr} {fb} {ud} {y}')
        # print(lr)
        time.sleep(1.5)
    print('end')


if __name__ == '__main__':
    drone_manager = DroneManager()
    drone_manager.takeoff()

    # For webcam input:
    cap = cv2.VideoCapture(0)
    threading.Thread(target=drone_command).start()
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
                        # print('r')
                        lr = '50'
                        #drone_manager.send_command('rc a 10')
                    elif hand_landmarks.landmark[mp_hands.HandLandmark(7).value].x * image_width < (image_width*2/3):
                        # print('m')
                        lr = '0'
                    elif hand_landmarks.landmark[mp_hands.HandLandmark(7).value].x * image_width < (image_width):
                        lr = '-50'
                        # print('l')

                        #drone_manager.send_command('rc a -10')
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
    a = 1
    #threading.Thread(target=drone_command)
    drone_manager.land()