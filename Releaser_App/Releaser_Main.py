import sys, time, threading
from Deque_Widget_Class import *
from Releaser_GUI import *
sys.path.append("../Queue_Handler")
from Queue_Class import *
sys.path.append("../Ethernet_Handler")
from UDP_Class import *


UDP_Manager = UDP_Class()
UDP_Manager.listenForMessages()
UDP_Manager.check_Connection()                               

   
deque = Queue_Class()  
def listenForUBIT():
   ## Delay to allow GUI to setup
   time.sleep(2)
   while(1):
      if UDP_Manager.RCV_UBIT_FLAG == 1:
         UDP_Manager.RCV_UBIT_FLAG_LOCK.acquire()
         UDP_Manager.RCV_UBIT_FLAG = 0
         UDP_Manager.RCV_UBIT_FLAG_LOCK.release()

         UDP_Manager.RCV_UBIT_BUFFER_LOCK.acquire()
         print "Listening Thread: ", UDP_Manager.RCV_UBIT_BUFFER
         window.dequeWidget.addToQueue(UDP_Manager.RCV_UBIT_BUFFER)
         UDP_Manager.RCV_UBIT_BUFFER = ""        
         UDP_Manager.RCV_UBIT_BUFFER_LOCK.release()
   
'''#   ENTRY POINT   #'''
if __name__ == "__main__":
   listenThread = threading.Thread(target=listenForUBIT)
   listenThread.daemon = True
   listenThread.start()
   app = QtGui.QApplication(sys.argv)
   app.setStyle(QtGui.QStyleFactory.create("plastique"))     
   window = ReleaserGUI()
   sys.exit(app.exec_())

   
   