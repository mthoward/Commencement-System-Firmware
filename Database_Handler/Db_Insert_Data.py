import MySQLdb

DB_NAME = "UB_COMMENCE"
DB_PASSWD = "root"
DB_USER = "root"
DB_HOST = "localhost"

def db_inserter(data):
   db = MySQLdb.connect(DB_HOST, DB_USER, DB_PASSWD, DB_NAME)
   cursor = db.cursor()
   try:
      cursor.execute("""INSERT INTO students (ubit, file_path) VALUES (%s,%s)""",(data['ubit'],data['file_path']))
      db.commit()
   except:
      db.rollback()
   cursor.execute("""SELECT * FROM students;""")
   print type(cursor.fetchall())
   db.close()
new_data = {'ubit' : "sethkara", 
	'file_path' : "/Recordings/sethkara.wav"}

#db_inserter(new_data)
