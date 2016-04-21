import time
import threading
import os
from collections import OrderedDict

#from Database_Handler import Db_Class
from utils.UDP_Class import UDP_Class
from utils.Queue_Class import Queue_Class

udpm = UDP_Class()
queue = Queue_Class()
#dbm = Db_Class.Db_Class()

def listenForMessage():
    print 'Listen for message running'
    time.sleep(1)
    while(True):
    	time.sleep(0.1)
        if udpm.RCV_UBIT_FLAG == 1:
            # Reset existence flag
    	    udpm.RCV_UBIT_FLAG_LOCK.acquire()
    	    udpm.RCV_UBIT_FLAG = 0
    	    udpm.RCV_UBIT_FLAG_LOCK.release()
    	    
    	    # Get data from buffer
    	    udpm.RCV_UBIT_BUFFER_LOCK.acquire()
    	    ubit = udpm.RCV_UBIT_BUFFER
    	    udpm.RCV_UBIT_BUFFER = ''
    	    udpm.RCV_UBIT_BUFFER_LOCK.release()
    	    
    	    # Put data in queue
    	    #student = dbm.get({'ubit': ubit})
    	    try:
    	        print 'Ubit added: %s' % ubit
    	        wavpath = '../res/namewavs/%s.wav' % ubit
    	        queue.addToBottomOfQueue(wavpath)
    	    except TypeError:
    	    	# TODO this is where our contingency plan must go into action
    	        print 'No entry for student'


# Start thread
listenThread = threading.Thread(target=listenForMessage)
listenThread.daemon = True
listenThread.start()
receiveThread = threading.Thread(target=udpm.receiveMessage)
receiveThread.daemon = True
receiveThread.start()
print 'Threads started'

    
while(True):
    raw_input('Waiting for user input...:')
    wavpath = queue.removeFromTopOfQueue()
    try:
    	print 'Playing %s' % wavpath.split('/')[-1].split('.')[0]
	os.system('aplay %s' % wavpath)
    except AttributeError:
    	print 'Queue empty'
    