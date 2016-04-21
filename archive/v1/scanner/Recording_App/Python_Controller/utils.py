import os

def create_subfolder(folderName):
   directory = os.path.dirname(os.getcwd())
   recordingsFolder = os.path.join(directory, folderName)
   if(os.path.isdir(recordingsFolder) == False):
      try:
         os.mkdir("Recordings")
      except OSError as exception:
         print "Error"
         raise


def install_packages(package_file):
   packages = open(package_file)
   for package in packages:
      os.system(package)


def check_file_exists(filename):
   filename = os.path.dirname(os.getcwd()) + "/Recordings/" + filename
   print filename
   return os.path.exists(filename)
