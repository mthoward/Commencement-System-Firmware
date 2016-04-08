import MySQLdb

class Db_Class():
   def __init__(self):
      self.DB_NAME = "UB_COMMENCE"
      self.DB_PASSWD = "root"
      self.DB_USER = "root"
      self.DB_HOST = "localhost"
   
   def insert(self, data):
      db = MySQLdb.connect(self.DB_HOST, self.DB_USER, self.DB_PASSWD, self.DB_NAME)
      cursor = db.cursor()
      try:
         cursor.execute("""INSERT INTO students (ubit, file_path) VALUES (%s,%s)""",(data['ubit'],data['file_path']))
         db.commit()
         print "Insertion Successful"
      except:
         db.rollback()
         print "Insertion Unsuccessful"
      db.close()
   
   
   def get(self, data):
      db = MySQLdb.connect(self.DB_HOST, self.DB_USER, self.DB_PASSWD, self.DB_NAME)
      cursor = db.cursor()
      cursor.execute("""SELECT ubit, file_path FROM students WHERE ubit = %s;""", data['ubit'])
      result = cursor.fetchone()
      if result == None:
         print("ERROR: NOT ENTRY FOR",data['ubit'])
      #print(result)
      db.close()
      return result
   
   
   '''Create Table'''
   def generateTable(self):
      ''' Connects to Database'''
      handle = MySQLdb.connect(self.DB_HOST, self.DB_USER, self.DB_PASSWD, self.DB_NAME)
      cursor = handle.cursor()
      TABLES = {}

      '''File Path Table'''
      TABLES['Students'] = (
          "CREATE TABLE `students` ("
          "  `unique_id` int(11) NOT NULL AUTO_INCREMENT,"
          "  `ubit` varchar(16) NOT NULL UNIQUE,"
          "  `file_path` varchar(200) NOT NULL,"
          "  PRIMARY KEY (`unique_id`)"
          ") ENGINE=InnoDB")

      for name, table in TABLES.iteritems():
         try:
            print("Creating Table: {} ".format(name))
            cursor.execute(table)
         except MySQLdb.Error as err:
#            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
#               print("already exists.")
#            else:
#            print(err.msg)
	    print "Error: Already Exists"
         else:
            print("OK")
      handle.close()
   
   
   
