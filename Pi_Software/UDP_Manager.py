from UDP_Class import *
import time

ubits = ["sethkara", "adbooth", "mthoward"]

UDP_Manager = UDP_Class(other_Pi_IP = '169.254.104.90',
                        other_Pi_Port = 15555,
                        localIP = '169.254.199.241',
                        localPort = 15556,
                        socketTimeout = 100)
UDP_Manager.listenForMessages()                                
while(1):
   UDP_Manager.sendMessage("Im the scanner PI")
   time.sleep(3)
   
   
   
# Scanner Port = 15556
# Releaser Port = 15555
