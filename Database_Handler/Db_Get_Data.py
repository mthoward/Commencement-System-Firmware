import MySQLdb

DB_NAME = "UB_COMMENCE"
DB_PASSWD = "root"
DB_USER = "root"
DB_HOST = "localhost"

def db_get_data(data):
   db = MySQLdb.connect(DB_HOST, DB_USER, DB_PASSWD, DB_NAME)
   cursor = db.cursor()
   ubit = "sethkara"
   cursor.execute("""SELECT ubit, file_path FROM students WHERE ubit = %s;""", data['ubit'])
   result = cursor.fetchone()
   if result == None:
      print("ERROR: NOT ENTRY FOR",data['ubit'])
   print(result)
   db.close()
   return result

new_data = {'ubit' : "sethkara"}

db_get_data(new_data)
