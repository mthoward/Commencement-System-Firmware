import picamera
import subprocess
from UDP_Class import *
import time
from qr import *

UDP_Manager = UDP_Class(other_Pi_IP = '169.254.104.90',
                        other_Pi_Port = 15555,
                        localIP = '169.254.199.241',
                        localPort = 15556,
                        socketTimeout = 100)
UDP_Manager.listenForMessages() 
UDP_Manager.check_Connection()  


def scan():
    camera = picamera.PiCamera()

    camera.start_preview(fullscreen=False, window = (400, 240, 400, 240))
    while 1:
        camera.capture("image.jpg", use_video_port=True)
        while(decode_qr("image.jpg") == 'NULL'):
            camera.capture("image.jpg", use_video_port=True)
   
        send_message(decode_qr("image.jpg"))
        print (decode_qr("image.jpg"))
        subprocess.call(["rm", "image.jpg"])

def send_message(name):
                     
    UDP_Manager.sendMessage(name, UDP_Manager.UBIT_SCANNED_MESS)
    print name



