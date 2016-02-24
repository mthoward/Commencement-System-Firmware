from recording_app_class import *
import os
import platform
from utils import *

if __name__ == "__main__":
 
   ### Install necessary packages ###
   #install_packages("sound_packages.txt")
   
   ### Create Subfolder To Hold Recordings
   create_subfolder("../Recordings")
   app = Recording_Window(None)
   app.title('UB Commencement Recording App')
   
   ### Name Insertion Function
   UB_ids = open("sample_student_list.txt")
   for UB_id in UB_ids:
      app.UBITListbox.insert(END, UB_id)
      
      ## Check if a recording exists already
      if check_file_exists(UB_id.rstrip() + ".wav"):
         app.StatusListbox.insert(END, "SAVED")
         app.StatusListbox.itemconfig(END, bg="green", fg="white")
      else:
         app.StatusListbox.insert(END, "NONE")
         
   app.mainloop()