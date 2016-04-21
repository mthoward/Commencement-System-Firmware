""" populate_db.py
Script for populating database with UBITs and filepaths
These data files should be stored in the database eventually
"""

from os import path
import json

import Db_Class

DATA_DIR_PATH = '../../res/'

# Make database manager object
dbm = Db_Class.Db_Class()
dbm.generateTable()

# Populate database
cenDict = json.load(open(path.join(DATA_DIR_PATH, 'most_eligible_CEN.json')))
for ubit, student in cenDict.iteritems():
    #print ubit, ':', student['Name']
    dbm.insert({
        'ubit': ubit,
        'name': ubit
    })
