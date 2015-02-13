from bs4 import BeautifulSoup
import urllib.request

response = urllib.request.urlopen("http://www.bloomberg.com/markets/stocks/world-indexes/americas/")
html = response.read()
soup = BeautifulSoup(html)

table = soup.find("table")
headers = []

#Single out the headers
for header in table.find_all("th"):
    headers.append(header.text.strip())

body = table.find("tbody")
info = []

for row in body.find_all("tr"):
    data = row.find_all("td")
    for d in data:
        print(d.text.strip())

