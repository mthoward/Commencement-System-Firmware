""" /Student_Data_Aquisition/scraper/ubdir_scraper.py
Scraper for for getting UB students' UBIT names from http://www.buffalo.edu/directory/
Feel free to ignore any "E1102 selector('<*>') is not callable" errors you might
    get with a Python linter. It's totally callable. It's a weird class in
    general if you ask me, but it works
"""

from lxml import html
from lxml.cssselect import CSSSelector as selector
import requests
import os
from time import sleep
import json

QUERY_URL = 'http://www.buffalo.edu/directory/search'
QUERY_URL += "?query=%s"
QUERY_URL += "&affiliation=%s"
QUERY_URL += "&qualifier=%s"
QUERY_URL += "&perpage=%i"
QUERY_URL += "&start=0"

SLEEP_TIME = 2

def getQueryPageTree(query, perpage=1, affiliation='student', qualifier='lastname'):
    """
    Gets DOM tree from http://www.buffalo.edu/directory/ based on passed query
        criteria.
    Built to handle server overload, since the server hosting the directory
        tends to send bad gateway and/or a 'Too many connections.' page when
        getting frequent requests
    """
    # Request the page until the proper page is received
    # This sometimes requires wait times to let the server cool off
    while True:
        # Get query page, query page tree, and connection overload element
        queryPage = requests.get(QUERY_URL % (query, affiliation, qualifier, perpage))
        queryPageTree = html.fromstring(queryPage.content)
        connectionOverloadElement = queryPageTree.xpath("//p[text()='Too many connections.']")

        # Check for OK status code and connection overload
        if queryPage.status_code != 200:
            print "Status code not 'OK', sleeping for %i seconds" % SLEEP_TIME
            sleep(SLEEP_TIME)
        elif connectionOverloadElement:
            print "Too many connections, sleeping for %i seconds" % (SLEEP_TIME*3)
            sleep(SLEEP_TIME*3)
        else:
            # The query received should be good, return the DOM tree
            return queryPageTree


def getFullQueryResults(query, qualifier='lastname'):
    """
    Returns a DOM tree element object from http://www.buffalo.edu/directory/
        with the full list of results.
    Normally a query to the directory will return results in pages of 10 entries
        each, which is inconvenient to scrape. Hence, this function makes an
        initial request, gets the quantity of results, then makes a second
        request that returns the full list of results
    """
    # Make first request
    firstQueryTree = getQueryPageTree(query, qualifier=qualifier)

    # See if query results in any records. If not, raise NameError
    if selector('p.bodyalt')(firstQueryTree):
        print "No results found for %s '%s'" % (qualifier, query)
        raise NameError

    # Get number of entries
    resultCountElement = selector('p.result_count')(firstQueryTree)[0]
    resultCount = int(resultCountElement.text.split()[-1])

    # Get full list response
    return getQueryPageTree(query,
                            perpage=resultCount,
                            qualifier=qualifier)


def getUBIT(name, major):
    """
    """
    nameTokens = name.split()
    studentInfo = {
        'name': name,
        'firstName': nameTokens[0],
        'lastName': nameTokens[-1]
    }

    queryResultsTree = getFullQueryResults(studentInfo['lastName'])
    entryList = selector('ul.content_list')(queryResultsTree)[0]
    entryListElements = entryList.findall('li')

    matchingMajors = []
    studentNames = []
    for element in entryListElements:
        # student = {}
        studentName = element.find('h3').find('a').text.strip()
        # student['name'] = studentName
        studentNames.append(studentName)
    print sum(1 for studentName in studentNames if studentName.split()[0] == studentInfo['firstName'])

inFileName = os.path.join(os.getcwd(), 'UB_CEN_Seniors.txt')
with open(inFileName) as inFile:
    for line in inFile:
        getUBIT(line, "Computer Engineering")
        sleep(SLEEP_TIME)
