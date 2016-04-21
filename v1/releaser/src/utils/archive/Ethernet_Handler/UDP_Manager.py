from UDP_Class import *
import time

ubits = ["sethkara", "adbooth", "mthoward"]

### Home Testing - Lenovo
UDP_Manager = UDP_Class(other_Pi_IP = '192.168.1.6',
                        other_Pi_Port = 15555,
                        localIP = '192.168.1.151',
                        localPort = 15556,
                        socketTimeout = 100)
### Home Testing - Server
# UDP_Manager = UDP_Class(other_Pi_IP = '192.168.1.151',
                        # other_Pi_Port = 15556,
                        # localIP = '68.133.10.203',
                        # localPort = 15555,
                        # socketTimeout = 100)
# ### Releaser Pi
#UDP_Manager = UDP_Class(other_Pi_IP = '169.254.199.241',
                   # other_Pi_Port = 15556,
                   # localIP = '169.254.104.90',
                   # localPort = 15555,
                   # socketTimeout = 100)
# ### Scanner Pi
#UDP_Manager = UDP_Class(other_Pi_IP = '169.254.104.90',
                   # other_Pi_Port = 15555,
                   # localIP = '169.254.199.241',
                   # localPort = 15556,
                   # socketTimeout = 100)
UDP_Manager.listenForMessages()
UDP_Manager.check_Connection()                               
while(1):
   #UDP_Manager.sendMessage("Im the scanner PI", UDP_Manager.UBIT_SCANNED_MESS)
   #time.sleep(1)
   #UDP_Manager.sendMessage("Are you Alive", UDP_Manager.STATUS_REQUEST_MESS)
   time.sleep(5)
   
   
   
# Scanner Port = 15556
# Releaser Port = 15555