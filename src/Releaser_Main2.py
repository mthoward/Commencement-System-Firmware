#!/usr/bin/python
import sys, time, threading, json
from utils.Deque_Widget_Class import *
from utils.Releaser_GUI_V2 import *
from utils.Queue_Class import *
from utils.UDP_Class import *

def listenForUBIT():
   ## Delay to allow GUI to setup
   time.sleep(2)
   while(1):
      if UDP_Manager.RCV_UBIT_FLAG == 1:
	 # Reset flag
         UDP_Manager.RCV_UBIT_FLAG_LOCK.acquire()
         UDP_Manager.RCV_UBIT_FLAG = 0
	 ubit = UDP_Manager.RCV_UBIT_BUFFER
	 UDP_Manager.RCV_UBIT_BUFFER = ""
	 UDP_Manager.RCV_UBIT_FLAG_LOCK.release()
	 
	 if ubit not in studentDict:
	     UDP_Manager.sendMessage("Not Found", UDP_Manager.UBIT_RESPONSE_MESS)
	     # TODO handle this error better
	 else:
	     UDP_Manager.sendMessage("Received Successfully", UDP_Manager.UBIT_RESPONSE_MESS)

	 if ubit not in ubitSet:
	     ubitSet.add(ubit)
	     window.dequeWidget.addToQueue(ubit)
	     window.deque.addToBottomOfQueue(ubit)
	 

	 # Get wavpath from db and add to queue
	 #try:
	    #student = dbm.get({'ubit': ubit})
	    #print "Listener found:", ubit

	    #if ubit not in ubitSet:
	        #ubitSet.add(ubit)
		#window.dequeWidget.addToQueue(student[0])
	        #window.deque.addToBottomOfQueue(student[1])
	    #print window.deque.deque
	    #UDP_Manager.sendMessage("Received Successfully", UDP_Manager.UBIT_RESPONSE_MESS)
	 #except Exception as e:
 	    #print e
	    #print "Not Found"
	    #UDP_Manager.sendMessage("Not Found", UDP_Manager.UBIT_RESPONSE_MESS)    
	 
	 
'''#   ENTRY POINT   #'''
if __name__ == "__main__":
    # Start contact with scanner
    UDP_Manager = UDP_Class()
    UDP_Manager.listenForMessages()
    
    # Make set to avoid repeats
    ubitSet = set()
    
    # Look at JSON file to detect existence
    studentDict = json.load(open('utils/most_eligible_CEN.json'))

    listenThread = threading.Thread(target=listenForUBIT)
    listenThread.daemon = True
    listenThread.start()
    app = QtGui.QApplication(sys.argv)
    app.setStyle(QtGui.QStyleFactory.create("plastique"))     
    window = ReleaserGUI2()
    sys.exit(app.exec_())