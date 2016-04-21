from recording_app_class import *
import os
import platform
from utils import *

if __name__ == "__main__":
 
   ### Install necessary packages ###
   install_packages("sound_packages.txt")
   
   ### Create Subfolder To Hold Recordings
   create_subfolder("Recordings")
   app = Recording_Window(None)
   app.title('UB Commencement Recording App')
   
   ### Run Name Insertion Function
   UB_ids = open("sample_student_list.txt")
   for UB_id in UB_ids:
      app.listbox.insert(END, UB_id)
   
   app.mainloop()