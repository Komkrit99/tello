import cv2
import time
import logging
from djitellopy import Tello
import cv2
#Tello.LOGGER.setLevel(logging.DEBUG)
import mediapipe as mp
tello = Tello()
tello.connect()
print(tello.get_battery())
#time.sleep(5)
#tello.takeoff()
# time.sleep(5)
# tello.move_up(70)
# time.sleep(5)
# tello.move_left(70)
# time.sleep(5)
# tello.move_right(70)
# time.sleep(5)
# tello.move_forward(70)
# time.sleep(5)
# tello.move_back(70)
# time.sleep(5)

# tello.go_xyz_speed(200, 0, 0, 70)
# time.sleep(5)
# tello.go_xyz_speed(-200, 0, 0, 70)
# time.sleep(5)
# tello.go_xyz_speed(0, 200, 0, 70)
# time.sleep(5)
# tello.go_xyz_speed(0, -200, 0, 70)
# time.sleep(5)
# tello.go_xyz_speed(0, 0, 50, 50)
# time.sleep(5)
# tello.go_xyz_speed(0, 0, -50, 50)
# time.sleep(5)

#tello.streamon()

# tello.takeoff()
# # cap = tello.get_frame_read()
# # cap = cap.frame
# # cap = cv2.resize(cap, (640, 480))  
# # cv2.imshow('cap',cap)
"""
while True:
    try:
        cap = tello.get_frame_read()
        cap = cap.frame
        cap = cv2.resize(cap, (640, 480))  
        cv2.imshow('cap',cap)
        if cv2.waitKey(5) & 0xFF == 27:
            cv2.destroyAllWindows()
            #cap.release()
            break
    except Exception as err:
        print(err)
time.sleep(3)
tello.streamoff()
"""
#time.sleep(2)
#tello.land()
