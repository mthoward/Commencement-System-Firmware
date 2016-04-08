#!/usr/bin/python

from UBDirectoryScraper import UBDirectoryScraper as ubds

inFileName = 'input_files/eligible_CEN.txt'
outFileName = 'output_files/eligible_CEN.json'

scraper = ubds(inFileName, outFileName)
scraper.scrape()
