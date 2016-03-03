import sys, subprocess
from utils import *
from List_Class import *
from MicRecorder_Class import *
from RecordingWidget_Class import *

'''#   ENTRY POINT   #'''
if __name__ == "__main__":
   create_subfolder("../Recordings")
   app = QtGui.QApplication(sys.argv)
   app.setStyle(QtGui.QStyleFactory.create("plastique"))
      
   window = RecordingWidget()
    
   ### Populate List
   for x in range(0,5):
      window.list.addToList("sethkara"+str(x+1))
  
   window.list.addToList("adbooth")
   window.list.addToList("mthoward")
   window.list.addToList("adbooth")
   window.list.addToList("alimahmo")
   window.list.addToList("davidtow")
   window.list.sortItems(0)
   sys.exit(app.exec_())