from UDP_Class import *
import time
import random

ubits = ["sethkara", "adbooth", "mthoward"]

UDP_Manager = UDP_Class(other_Pi_IP = '169.254.104.90',
                        other_Pi_Port = 15555,
                        localIP = '169.254.199.241',
                        localPort = 15556,
                        socketTimeout = 100)
UDP_Manager.listenForMessages()
UDP_Manager.check_Connection()

#ubits['sethkara','adbooth','mthoward']

while(1):
   UDP_Manager.sendMessage(ubits[random.randint(0,2)], UDP_Manager.UBIT_SCANNED_MESS)
   time.sleep(3)
   
   
   
# Scanner Port = 15556
# Releaser Port = 15555
