""" /Student_Data_Aquisition/UBDirectoryScraper.py
Scraper for for getting UB students' UBIT names from
    http://www.buffalo.edu/directory/
Feel free to ignore any "E1102 selector('<*>') is not callable" errors you might
    get with a Python linter. It's totally callable. It's a weird class in
    general if you ask me, but it works.
"""

from time import sleep, time
import datetime
from lxml import html
from lxml.cssselect import CSSSelector as selector
from pprint import PrettyPrinter
import json

import requests

START_TIME = time()
WAIT_TIME = 2
PP = PrettyPrinter(indent=4)

QUERY_URL = "http://www.buffalo.edu/directory/"
QUERY_URL += "search?query=%s"
QUERY_URL += "&affiliation=student"
QUERY_URL += "&qualifier=%s"
QUERY_URL += "&perpage=%i"
QUERY_URL += "&start=0"


def getQueryPageTree(query, perpage=1, qualifier='lastname'):
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
        queryPage = requests.get(QUERY_URL % (query, qualifier, perpage))
        queryPageTree = html.fromstring(queryPage.content)
        connectionOverloadElement = queryPageTree.xpath("//p[text()='Too many connections.']")

        # Check for OK status code and connection overload
        if queryPage.status_code != 200:
            print "Status code not 'OK', sleeping for %i seconds" % WAIT_TIME
            sleep(WAIT_TIME)
        elif connectionOverloadElement:
            print "Too many connections, sleeping for %i seconds" % (WAIT_TIME*3)
            sleep(WAIT_TIME*3)
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
    return getQueryPageTree(query, perpage=resultCount, qualifier=qualifier)


def dl2dict(dl):
    """
    Returns a dict built from a `dl` object
    """
    if not isinstance(dl, html.HtmlElement) or dl.tag != 'dl':
        raise TypeError("An xml.html.HtmlElement 'dl' object is required")
    dlTextList = [element.text for element in list(dl)]
    return dict([dlTextList[i:i+2] for i in xrange(0, len(dlTextList), 2)])


def getUBIT(targetName, targetMajor):
    """
    Returns a dict of students' info, keyed by their UBIT name, based on name
        and major criteria
    This function makes the query request to UB Directory, parses the DOM tree,
        and loops over the entries, filtering by major and name matching.
    Not sure how reliable the returned data is, based on name matching. Some of
        the names provided by the input file may not completely match the names
        from the entries on the UB Directory, due to personal updates
        introducing nicknames, spelling corrections, or other unpredictable
        variations in name
    It also returns all likely matches, instead of one sure match every time.
        This is due to the fact that shared surnames might exist in the same
        major.
    If no viable match is discovered, an error is thrown to alert the calling
        scope.
    """
    # Handle target information
    nameTokens = targetName.split()
    target = {
        'name': targetName,
        'firstName': nameTokens[0],
        'lastName': nameTokens[-1],
        'major': targetMajor,
        'tokens': nameTokens
    }

    # Make list of `li` entries from UB directory query
    queryResultsTree = getFullQueryResults(target['lastName'])
    entryList = selector('ul.content_list')(queryResultsTree)[0]
    entryListElements = entryList.findall('li')

    # Loop over `li`s and check each entry for match with target info
    candidates = {}
    for liElement in entryListElements:
        # Get the 'item_info' `dl` from the entry and turn it into a dict for
        #   easy access
        descriptionListElement = selector('dl.item_info')(liElement)[0]
        candidate = dl2dict(descriptionListElement)
        # Add their name
        candidateName = liElement.find('h3').find('a').text.strip()
        candidate['Name'] = candidateName
        # Add their UBIT
        queryPart = liElement.find('h3').find('a').get('href').split('/')[-1]
        candidateUBIT = queryPart.split('&')[0].split('?')[0]
        candidate['UBIT'] = candidateUBIT
        # Update their email
        candidate['Email'] = candidateUBIT + '@buffalo.edu'

        # Ignore candidates not belonging to the right department
        if target['major'].lower() != candidate['Department'].lower():
            continue
        # ...and those whose last name does not exist in their entry name
        if target['lastName'].lower() not in candidate['Name'].lower():
            continue
        # # ...same as above, but for first name
        # if not target['firstName'].lower() in candidate['Name'].lower():
        #     continue

        # Candidate made it through tests, add them
        candidates[candidateUBIT] = candidate

    if not candidates:
        raise KeyError("No viable candidates found for %s" % targetName)
    else:
        return candidates


# inFileName = os.path.join(os.getcwd(), 'input_files/UB_CEN_Seniors.txt')
# students = {}
# unfoundStudents = []
# queriedLastNames = set()
# with open(inFileName) as inFile:
#     for line in inFile:
#         name = line.replace('\n', '')
#         lastName = name.split()[-1]
#         if lastName in queriedLastNames:
#             print "%s's last name (%s) has been queried, skip" \
#                 % (name, lastName)
#             continue
#         queriedLastNames.add(lastName)
#         print '\n\n' + name + ':'
#         try:
#             matches = getUBIT(name, 'Computer Engineering')
#             students.update(matches)
#             PP.pprint(matches)
#         except IndexError as e:
#             # Try again because it was likely an HTML retrieval error
#             print "Index error received for %s" % name
#             print e
#             print "Adding %s to unfound students list" % name
#             unfoundStudents.append(name)
#         except KeyError as e:
#             # No viable candidate found in getUBIT
#             print e
#             print "Adding %s to unfound students list" % name
#             unfoundStudents.append(name)
#         sleep(WAIT_TIME)

class UBDirectoryScraper:
    results = {}
    queriedSurNames = set()
    unfoundStudents = []

    def __init__(self, inFileName, outFileName=None, infoFileName=None, targetMajor='Computer Engineering'):
        self.inFileName = inFileName
        self.outFileName = outFileName
        self.infoFileName = infoFileName
        self.targetMajor = targetMajor

    def scrape(self):
        # Guard against empty inputs
        if not self.inFileName:
            raise Exception('Need to set an input file (set with `UBDirectoryScraper.infile`)')
        if not self.outFileName:
            self.outFileName = datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + '_out.json'
        if not self.infoFileName:
            self.infoFileName = datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + '_info.txt'

        startTime = time()
        with open(self.inFileName) as infile:
            for line in infile:
                # Parse line for names
                name = line.strip()
                print '%s:' % name
                surName = name.split()[-1]
                if surName in self.queriedSurNames:
                    print '    Already queried'
                    continue

                # Add to queried list to avoid over requesting website
                self.queriedSurNames.add(surName)

                # Scrape for name
                try:
                    matches = getUBIT(name, self.targetMajor)
                    print '    ' + str(matches)
                    self.results.update(matches)
                except (IndexError, KeyError):
                    print '    Not found'
                    self.unfoundStudents.append(name)

                # Sleep because the UB Directory is <em>WEAK</em>
                sleep(WAIT_TIME)

        # Write results file
        with open(self.outFileName, 'w') as outFile:
            json.dump(self.results, outFile)

        # Write info file
        unfoundString = 'Students not found:\n    ' + '\n    '.join(self.unfoundStudents)
        elapsedTime = str(time() - startTime)
        with open(self.infoFileName, 'w') as infoFile:
            infoFile.write('Elapsed time: %s' % elapsedTime)
            infoFile.write('\n\n')
            infoFile.writelines(unfoundString)
