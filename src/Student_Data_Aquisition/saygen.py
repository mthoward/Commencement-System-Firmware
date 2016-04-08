#!/usr/bin/python

import json
import os

sayCommand = 'say -o %s.wav --data-format=LEUI8@22000 "%s"'

with open('output_files/most_eligible_CEN.json', 'r') as cenFile:
    students = json.load(cenFile)

for ubit, studentDict in students.iteritems():
    print studentDict['Name']
    os.system(sayCommand % ('output_files/namewavs/%s' % ubit, studentDict['Name']))
