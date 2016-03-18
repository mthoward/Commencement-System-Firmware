import pyqrcode
import qrtools
import picamera
import subprocess
from UDP_Class import *
import time
camera = picamera.PiCamera()
UDP_Manager = UDP_Class(other_Pi_IP = '169.254.104.90',
                        other_Pi_Port = 15555,
                        localIP = '169.254.199.241',
                        localPort = 15556,
                        socketTimeout = 100)

def encode_qr(data):
    qr = pyqrcode.create(data)
    filename = data + ".png"
    qr.png(filename, scale=2)


def decode_qr(filename):
    qr = qrtools.QR()
    qr.decode(filename)
    return qr.data

#encode_qr("mthoward")
#print (decode_qr("mthoward.png"))



def scan():
     
    UDP_Manager.listenForMessages()                       

    camera.start_preview(fullscreen=False, window = (400, 0, 400, 240))
    camera.capture("image.jpg")
    while(decode_qr("image.jpg") == 'NULL'):
            camera.capture("image.jpg")
    camera.stop_preview()
    UDP_Manager.sendMessage(decode_qr("image.jpg"))
    print (decode_qr("image.jpg"))
    subprocess.call(["rm", "image.jpg"])
