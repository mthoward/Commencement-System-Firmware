import sys
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
   for x in range(0,15):
      window.list.addToList("sethkara"+str(x+10))
  
   window.list.addToList("adbooth")
    
   window.list.sortItems(0)

   sys.exit(app.exec_())