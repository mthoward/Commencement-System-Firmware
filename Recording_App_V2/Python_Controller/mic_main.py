import sys, subprocess
from utils import *
from List_Class import *
from MicRecorder_Class import *
from RecordingWidget_Class import *


def populateList():
   #os.system("python ../../Student_Data_Aquisition/scraper/scraper.py")
   ### Name Insertion Function
   return populate_from_JSON("../../Student_Data_Aquisition/scraper/UB_CEN_UBITs.json")
   

'''#   ENTRY POINT   #'''
if __name__ == "__main__":
   create_subfolder("../Recordings")
   app = QtGui.QApplication(sys.argv)
   app.setStyle(QtGui.QStyleFactory.create("plastique"))
      
   window = RecordingWidget()
    
   ### Populate List
   UBITs = populateList()
   for x in range(0,len(UBITs)):
      window.list.addToList(UBITs[x])
   window.list.sortItems(0)
   sys.exit(app.exec_())