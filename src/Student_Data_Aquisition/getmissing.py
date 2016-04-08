#!/usr/bin/python

import json

# Get unfound students
with open('output_files/2016-03-25_16-33-52_info.txt') as infoFile:
    studentListString = infoFile.read().split(':\n')[1]
    studentNames = studentListString.replace('    ', '').split('\n')

# Create new manual student dict
students = {}
for studentName in studentNames:
    ubit = raw_input("%s's UBIT: " % studentName)
    if not ubit:
        students[ubit] = None
    else:
        students[ubit] = {
            'UBIT': ubit,
            'Email': ubit + '@buffalo.edu',
            'Title': 'Student',
            'Department': 'Computer Engineering',
            'Name': studentName
        }

# Update final dict
with open('output_files/eligible_CEN.json') as cenFile:
    studentDict = json.load(cenFile)

studentDict.update(students)
with open('output_files/all_CEN.json', 'w') as allFile:
    json.dump(studentDict, allFile)
