""" populate_db.py
Script for populating database with UBITs and filepaths
These data files should be stored in the database eventually
"""

from os import path
import json

import Db_Class

DATA_DIR_PATH = '/home/adbooth/Commencement-System-Firmware/src/Student_Data_Aquisition/output_files/'

# Make database manager object
dbm = Db_Class.Db_Class()
dbm.generateTable()

# Populate database
cenDict = json.load(open(path.join(DATA_DIR_PATH, 'most_eligible_CEN.json')))
for ubit, student in cenDict.iteritems():
    wavFileName = ubit + '.wav'
    wavFilePath = path.join(DATA_DIR_PATH, 'namewavs', wavFileName)
    dbm.insert({
        'ubit': ubit,
        'file_path': wavFilePath
    })
