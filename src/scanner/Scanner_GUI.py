from scanner_GUI_class import *
import os
import platform
from utils import *
from qr import *
from scanner import *
import thread

if __name__ == "__main__":
 
   app = Scanner_Window(None)
   app.title('UB Commencement')

   thread.start_new_thread(scan,())

   app.mainloop()
   thread.exit()
