import os
import json

def create_subfolder(folderName):
   recordingsFolder = os.path.join(os.getcwd(), folderName)
   recordingsFolder = os.path.normpath(recordingsFolder)
   print recordingsFolder
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
# =======
   # filename = os.path.dirname(os.getcwd()) + "/Recordings/" + filename
   # print filename
   # return os.path.exists(filename)

   
def populate_from_JSON(filename):
   UBIT =[]
   filepath = os.path.join(os.getcwd(),"../Recordings/"+filename)
   filepath = os.path.normpath(filepath)
   with open(filepath) as jsonFile:
      students = json.load(jsonFile)
      for stu in students:
         repack = json.dumps(students[stu])
         unpack = json.loads(repack)
         try:
            ubit = unpack['ubit']
            if len(ubit) > 8:
               print "-----ERROR----- > " + str(stu)
            else:
               UBIT.append(ubit)
         except KeyError, e:
            print "-----ERROR----- > " + str(stu)
   return UBIT      