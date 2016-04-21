""" scanner/__init__.py
Starts scanner software
"""

# Standard imports
import threading
# Package imports
# from picamera import PiCamera
# Local imports
from utils.UDP_Class import UDP_Class
from qr import qrencode, qrdecode
from Student import Student
from Squeue import Queue

# IO objects
camera = PiCamera()
udpm = UDP_Class(localIP = '169.254.199.241',
                 localPort = 15556,
                 other_Pi_IP = '169.254.104.90',
                 other_Pi_Port = 15555,
                 socketTimeout = 100)

# Data structures
walkedStudents = set()
studentQueue = Queue()


print 'Scanner software starting...'
while True:
    pass
    break
