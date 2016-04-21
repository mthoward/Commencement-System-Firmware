#!/usr/bin/python
""" Scraper for getting students' UBIT names """

from lxml import html
import requests
import os
from time import sleep
import json

QUERY_URL = "http://www.buffalo.edu/directory/search?query=%s&affiliation=student&qualifier=general&perpage=%i&start=0"
SLEEP_TIME = 2

def getRequestDomTree(lastName, perPage=1):
    while True:
        query = requests.get(QUERY_URL % (lastName, perPage))
        queryTree = html.fromstring(query.content)

        if query.status_code != 200:
            print query
            print "Sleeping for %i seconds..." % SLEEP_TIME
            sleep(SLEEP_TIME)
        elif queryTree.xpath("//p[text()='Too many connections.']"):
            print "Too many connections"
            print "Sleeping for %i seconds..." % (SLEEP_TIME*3)
            sleep(SLEEP_TIME*3)
        else:
            return queryTree


def lastNameScrape(lastName, major):
    # Get first response
    firstQueryTree = getRequestDomTree(lastName)

    # See if this query returns any records. If not, exit
    if firstQueryTree.xpath("//span[@class='bodyalt']"):
        # TODO Maybe query with other data?
        print "No results found for last name '%s'" % lastName
        return {"key": "not found"}

    # Some queries will result in multiple pages of entries. This gets the number of entries
    resultCountText = firstQueryTree.xpath("//p[@class='result_count']")[0].text
    resultCount = int(resultCountText.split()[-1])

    # Get non-naive query response using `resultCount`
    entryListTree = getRequestDomTree(lastName, perPage=resultCount)
    # Grab unordered list element that contains the list element entries
    entryUnorderedListElement = entryListTree.xpath("//ul[contains(concat(' ', normalize-space(@class), ' '), ' content_list ')]")[0]
    # Make list of entry list elements
    entries = entryUnorderedListElement.findall("li")

    # Loop over list elements and grab major, name, and email info
    candidates = {}
    for entry in entries:
        # Make candidate object and add to candidates
        candidate = {}
        entryName = entry.find("h3").find("a").text.strip()
        candidate["name"] = entryName
        candidates[entryName] = candidate

        # Loop through element in 'item_info' `dl` element
        item_info_tags = list(entry.find("dl"))
        for count in xrange(len(item_info_tags)):
            # If department `dt`, get next `dd` for major info
            if item_info_tags[count].text == "Department":
                # print "Major found for %s" % entryName
                entryMajor = item_info_tags[count+1].text
                if entryMajor != major:
                    # print "Deleting %s's entry" % entryName
                    del candidates[entryName]
                    continue
                print "Adding %s" % entryName
                candidate["major"] = entryMajor

            # If email `dt`, get next `dd` for email info
            if item_info_tags[count].text == "Email":
                # print "Email found for %s" % entryName
                entryEmailScriptText = item_info_tags[count+1].find("script").text
                for part in entryEmailScriptText.split(","):
                    if "makeEmail" in part:
                        candidate["ubit"] = part.split('"')[1]
                        break

    return candidates

# Scripting starts here
currentDirectory = os.getcwd()
inputFileName = os.path.join(currentDirectory, "UB_CEN_Seniors.txt")
outputFileName = os.path.join(currentDirectory, "UB_CEN_UBITs.json")

studentDict = {}
with open(inputFileName) as inputFile:
    for line in inputFile:
        sleep(SLEEP_TIME)
        last_name = line.split()[-1]
        print "\n\n" + last_name + ":"
        student = lastNameScrape(last_name, "Computer Engineering")
        print student
        studentDict.update(student)

with open(outputFileName, 'w') as outputFile:
    json.dump(studentDict, outputFile)
