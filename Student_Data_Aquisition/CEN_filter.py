""" Filtering for CEN majors in list from http://www.cse.buffalo.edu/people/students/index.php """

import os
from sys import argv

scriptName, inputFileName, outputFileName = argv

CURRENT_DIRECTORY = os.getcwd()
INPUT_FILE_PATH = os.path.join(CURRENT_DIRECTORY, inputFileName)
OUTPUT_FILE_PATH = os.path.join(CURRENT_DIRECTORY, outputFileName)

outputFile = open(OUTPUT_FILE_PATH, 'w+')
with open(INPUT_FILE_PATH) as inputFile:
    for line in inputFile:
        if "Computer Engineering" in line:
            outputFile.write(line.split(',')[0].strip() + '\n')
