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

#Add new header
headers.append("Original Value")

body = table.find("tbody")
newRecordsInFile = []
newRecordsInFile.append("\t".join(headers))

## Helper methods ##
def calculateOriginalValue(value, change):
    valNum = float(value)
    chgNum = float(change)
    return valNum - chgNum

def sanitize(string):
    if(string[0] == '+'):
        return string[1:]
    return string
###

for row in body.find_all("tr"):
    newEntriesInRecord = []
    data = row.find_all("td")
    value = ""
    change = ""
    for d in range(len(data)):
        newEntriesInRecord.append(data[d].text)
        if(d == 1):
            value = data[d].text
        elif(d == 2):
            change = sanitize(data[d].text)

    originalValue = str(calculateOriginalValue(value.replace(',',''), change.replace(',','')))
    newEntriesInRecord.append(originalValue)
    newEntriesInRecord = "\t".join(newEntriesInRecord)
    newRecordsInFile.append(newEntriesInRecord)

print("Writing modified data to new file....")

f = open("modified-data.txt", "w")

for record in newRecordsInFile:
    f.write(record + "\n")

f.close()








