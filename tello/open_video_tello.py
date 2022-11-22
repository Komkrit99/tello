import logging
import socket
import sys
import time
import cv2
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


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


if __name__ == '__main__':
    drone_manager = DroneManager()
    drone_manager.send_command('streamon')
    tello_video = cv2.VideoCapture('https://0.0.0.0:11111')

    while True:
        try:
            ret, frame = tello_video.read()
            if ret:
                cv2.imshow(frame)
            if cv2.waitKey(5) & 0xFF == 27:
                break
        except Exception as err:
            print(err)
            break
    tello_video.release()
    cv2.destroyAllWindows()
    drone_manager.send_command('streamoff')
