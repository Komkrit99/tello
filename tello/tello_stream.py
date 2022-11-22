import socket
import cv2
print('start')
tello_video = cv2.VideoCapture('upd://@0.0.0.0:11111')
print(tello_video)
while True:
    try:
        ret, frame = tello_video.read()
        if ret:
            cv2.imshow(frame)
        else:
            #print('no ret')
            pass
        if cv2.waitKey(5) & 0xFF == 27:
                break
    except Exception as err:
        print(err)
tello_video.release()
cv2.destroyAllWindows()