from Db_Class import *

db_manager = Db_Class()
data = {'ubit':"sethkars",
	'file_path':"/filepath_here/fkjerlf.wav"}

db_manager.generateTable()
db_manager.insert(data)
db_manager.get({'ubit':"sethkars"})
