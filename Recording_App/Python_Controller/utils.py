import os

def create_subfolder(folderName):
   recordingsFolder = os.path.join(os.getcwd(), folderName)
   recordingsFolder = os.path.normpath(recordingsFolder)
   if(os.path.isdir(recordingsFolder) == False):
      try:
         os.mkdir("../Recordings")
      except OSError as exception:
         print "Error"
         raise

         
def install_packages(package_file):
   packages = open(package_file)
   for package in packages:
      os.system(package)
 
 
def check_file_exists(filename):
   filepath = os.path.join(os.getcwd(),"../Recordings/"+filename)
   filepath = os.path.normpath(filepath)
   return os.path.exists(filepath)