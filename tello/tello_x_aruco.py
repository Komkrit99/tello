import cv2
import time
import logging
from djitellopy import Tello
import cv2
#Tello.LOGGER.setLevel(logging.DEBUG)

tello = Tello()
tello.connect()
# Tello.land()
tello.streamon()
print(tello.get_battery())
# cap = tello.get_frame_read()
# cap = cap.frame
# cap = cv2.resize(cap, (640, 480))  
# cv2.imshow('cap',cap)
while True:
    try:
        cap = tello.get_frame_read()
        cap = cap.frame
        cap = cv2.resize(cap, (640, 480))  
        cv2.imshow('cap',cap)
        if cv2.waitKey(5) & 0xFF == 27:
                break
    except Exception as err:
        print(err)
cap.release()
cv2.destroyAllWindows()