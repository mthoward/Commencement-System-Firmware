import sys, subprocess, time
from utils import *
from List_Class import *
from MicRecorder_Class import *
from RecordingWidget_Class import *


def populateList():
   ### Run scraper
   # origWD = os.getcwd() # remember our original working directory
   # relPathToLaunch = '../../Student_Data_Aquisition/scraper'
   # os.chdir(os.path.join(os.path.abspath(sys.path[0]), relPathToLaunch))
   # proc = subprocess.Popen(['python','scraper.py'], #cwd='../../Student_Data_Aquisition/scraper/
                        # stdout=subprocess.PIPE,
                        # ) 
   # os.chdir(origWD) # get back to our original working directory
   
   # timer = 0
   # while(timer != 3):
      # time.sleep(1)
      # timer += 1
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
