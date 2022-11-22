import cv2
import mediapipe as mp
import time
import time
import logging
from cv2 import aruco
from djitellopy import Tello
import threading
import keyboard
import sys, select, os
if os.name == 'nt':
  import msvcrt, time
else:
  import tty, termios
  settings = termios.tcgetattr(sys.stdin)
#Tello.LOGGER.setLevel(logging.DEBUG)
lr = 0
fb = 0
ud = 0
y = 0
a = 0

tello = Tello()
tello.connect()
#tello.streamon()
def control_drone():
  global lr,fb,ud,y,a
  while a == 0:
    tello.send_rc_control(lr,fb,ud,y)
    #print(lr,fb,ud,y)
    time.sleep(0.1)
def getKey():
    if os.name == 'nt':
        timeout = 0.1
        startTime = time.time()
        while(1):
            if msvcrt.kbhit():
                if sys.version_info[0] >= 3:
                    return msvcrt.getch().decode()
                else:
                    return msvcrt.getch()
            elif time.time() - startTime > timeout:
                return ''

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key
threading.Thread(target=control_drone).start()
print('start')
mini = -100
maxi = 100
while True:

  try:
    key = getKey()
    if key =='w' and fb<100:
        #print('hahahahahah')
        if fb <0:
            fb = 0
        fb += 10
    elif key =='d'and lr<maxi:
        if lr <0:
            lr = 0
        lr += 10
    elif key =='t'and lr<maxi:
        tello.takeoff() 
    elif key =='s'and fb>mini:
        fb -= 10
        if fb > 0:
            fb = 0
    elif key =='a'and lr>mini:
        if lr >0:
            lr = 0
        lr -= 10
    elif key =='e'and y<maxi:
        if y <0:
            y = 0
        y += 10
    elif key =='q'and y>mini:
        if y >0:
            y = 0
        y -= 10
    elif key =='c'and ud<maxi:
        if ud <0:
            ud = 0
        ud += 10
    elif key =='v'and ud>mini:
        if ud >0:
            ud = 0
        ud -= 10
    elif key =='z':
        fb = 0
        lr = 0
        ud = 0
        y = 0
        a = 1
        break
    else:
        fb = 0
        lr = 0
        ud = 0
        y = 0
    
  except:
    pass
        # if key ==('q'):  # if key 'q' is pressed 
        #     print('You Pressed A Key!')
        #     break  # finishing the loop

    #cap.release()


tello.land()
# tello.streamoff()