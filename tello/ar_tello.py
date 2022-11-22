from dis import dis
from turtle import distance
import cv2
from cv2 import destroyAllWindows
import mediapipe as mp
import time
import cv2
import time
import logging
from cv2 import aruco
from djitellopy import Tello
import cv2
import threading
import numpy as np
#Tello.LOGGER.setLevel(logging.DEBUG)
lr = 0
fb = 0
ud = 0
ya = 0
a = 0
num_temp = 0
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
tello = Tello()
tello.connect()
tello.streamon()
tello.takeoff() 
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
def control_drone():
  global lr,fb,ud,ya,a
  while a == 0:
    tello.send_rc_control(lr,fb,ud,ya)
    #print(lr,ud)
    time.sleep(0.3)
def target_detect(ids,corners,temp_num):
    posi = []
    try:
        if len(ids) != 0 :
            num = 0
            # print(ids)
            print('---------')
            for a in ids:
                #print(num)
                #print(a[0])
                if a[0] == temp_num:
                    posi =corners[num][0]
                    #print(posi)
                num+=1
        # else:
        #     posi = []
    except:
        pass
    return  posi
def num_step():
      stp = [3,0,3,0,3,0,3]
      global num_temp

      time.sleep(10)
      for a in range(len(stp)):
            time.sleep(4.5)
            num_temp = stp[a]
            
threading.Thread(target=control_drone).start()
threading.Thread(target=num_step).start()
pos = [0,0,0]
#print('start')

def get_possi():
      print('start')
      while True:
            cap = tello.get_frame_read()
            cap = cap.frame
            image_width  = 640   # float `width`
            image_height = 480  # float `height`
            image = cv2.resize(cap, (image_width, image_height))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
            parameters =  aruco.DetectorParameters_create()
            corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
            frame_markers = aruco.drawDetectedMarkers(image.copy(), corners, ids)
            # print('----------')
            # print(len(corners))
            print(num_temp)
            posi = target_detect(ids,corners,num_temp)
            if len(posi) != 0:
                  #print(posi)
                  x = (posi[0][0] + posi[3][0]) /2
                  y = (posi[0][1] + posi[3][1]) /2
                  dist =round((np.abs(posi[0][0]-posi[1][0])+np.abs(posi[0][0]-posi[2][0]))/2)
                  print(x,y,dist)
                  global lr,fb,ud,ya,a
                  if x   < (image_width*2/5):
                  #print('r')
                        pos[0] = 1
                        lr = -20
                  elif x   < (image_width*3/5):
                  #print('m')
                        pos[0] = 2
                        lr = 0
                  elif x   < (image_width):
                  #print('l')
                        pos[0] = 3
                        lr = 20
                  if y  < (image_height*2/5):
                        pos[0] = 1
                        # print('t')
                        ud = 20
                  elif y  < (image_height*3/5):
                        pos[0] = 2
                        # print('m')
                        ud = 0
                  elif y  < (image_height):
                        pos[0] = 3
                        # print('b')
                        ud = -20
                  if dist > 40:
                        pos[0] = 1
                        fb = -50
                        #print('b')
                  elif dist < 30:
                        pos[0] = 2
                        fb = 50
                        #print('f')
                  else:
                        fb = 0
                        pos[0] = 3
                        #print('s')
                  #print(pos)
                  # print(dist)
            else:

                  lr = 0
                  ud = 0
                  fb = 0
                  ya = 0

            cv2.imshow('MediaPipe Hands', frame_markers)
            if cv2.waitKey(33) == ord('a'):
            #a = 1
                  lr = 0
                  ud = 0
                  fb = 0
                  ya = 0
                  cv2.destroyAllWindows()
                  #cap.release()
                  break 
get_possi()
# print('up')
# lr = 0
# ud = 30
# fb = 0
# ya = 0
# time.sleep(3)
# lr = 0
# ud = 0
# fb = 0
# ya = 0
# #time.sleep(2)
# #get_possi()
# time.sleep(3)
# # print('up')
# # lr = 0
# # ud = 30
# # fb = 0
# # ya = 0
# # time.sleep(5)
# # #time.sleep(5)
# print('left')

# lr = -30
# ud = 0
# fb = 0
# ya = 0
# time.sleep(5)
# print('left')

# lr = 0
# ud = 0
# fb = 30
# ya = 0
# time.sleep(5)
# print('left')

# lr = 30
# ud = 0
# fb = 0
# ya = 0
# time.sleep(5)
# print('left')

# lr = 0
# ud = 0
# fb = -30
# ya = 0
# time.sleep(5)
# print('right')

# lr = 0
# ud = 0
# fb = 0
# ya = 0
# time.sleep(5)
# lr = 0
# ud = 0
# fb = 0
# ya = 30
# time.sleep(5)
print('end')

lr = 0
ud = 0
fb = 0
ya = 0
time.sleep(2)
# tello.go_xyz_speed(50, -50, 0, 30)
# time.sleep(5)
# tello.flip_forward()
# time.sleep(5)
# tello.flip_back()
# time.sleep(5)
# tello.go_xyz_speed(-50, 50, 0, 30)
#time.sleep(5)
# get_possition()
a = 1
tello.land()
tello.streamoff()