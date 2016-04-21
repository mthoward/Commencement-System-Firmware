import requests
from lxml import html

query = requests.get("http://localhost:8000/finding_people_error.html")
tree = html.fromstring(query.content)

connp = tree.xpath("//p[text()='Too many connections.']")
print "YUP" if connp else "NOPE"
