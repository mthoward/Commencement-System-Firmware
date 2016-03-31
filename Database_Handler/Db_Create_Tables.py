import MySQLdb


''' Connects to Database'''
handle = MySQLdb.connect(user='root',
                              passwd='root',
                              host='localhost',
                              db='UB_COMMENCE')
cursor = handle.cursor()

DB_NAME = 'UB_COMMENCE'
TABLES = {}

'''Example Table'''
TABLES['Students'] = (
    "CREATE TABLE `students` ("
    "  `unique_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `ubit` varchar(16) NOT NULL,"
    "  `file_path` varchar(200) NOT NULL,"
    "  PRIMARY KEY (`unique_id`)"
    ") ENGINE=InnoDB")


'''Create Table'''
def createTables(tableList):
   for name, table in TABLES.iteritems():
      try:
         print("Creating Table: {} ".format(name))
         cursor.execute(table)
      except mysqldb.Error as err:
         if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
         else:
            print(err.msg)
      else:
         print("OK")

createTables(TABLES)

handle.close()
