from cv2 import aruco
import numpy as np
import cv2

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

cap = cv2.VideoCapture(0)
def target_detect(ids,corners,temp_num):
    posi = []
    try:
        if len(ids) != 0 :
            num =0
            for a in ids:
                if a[0] == temp_num:
                    posi =corners[0][num]
                num+=1
        # else:
        #     posi = []
    except:
        pass
    return  posi
while True:
    try:
        ret,frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        parameters =  aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
        # if len(corners) != 0:
        #     x = (corners[0][0][0][0] + corners[0][0][3][0]) /2
        #     y = (corners[0][0][0][1] + corners[0][0][3][1]) /2

        #     print(x,y)
        print(target_detect(ids,corners,1))
        # try:
        #     for a in ids:
        #         print(corners[a])
        # #print(ids,corners)
        
            #frame_markers = cv2.drawMarker(frame_markers,corners[0][0][0],color=(0,255,0), markerType=cv2.MARKER_CROSS, thickness=2)

        cv2.imshow('MediaPipe Hands', cv2.flip(frame_markers, 1))
        if cv2.waitKey(33) == ord('a'):
            cap.release()
            cv2.destroyAllWindows()
            break
    except:
        pass