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

## Helper methods ##
def calculateOriginalValue(value, change, percentChange):
    value = float(value)
    change = float(value)
    percentChange = float(value)
    if(percentChange[0] == '-'):
        return value + (change / percentChange)
    return value - (change / percentChange)

def sanitize(index, string):
    result = ""
    if(string[0] == '+'):
        result = string[1:]

    if(index == 2):
        return result
    else:
        return result[:len(string)-1]
###

for row in body.find_all("tr"):
    newEntriesInRecord = []
    data = row.find_all("td")
    value = ""
    change = ""
    percentChange = ""
    for d in range(len(data)):
        newEntriesInRecord.append(data[d])
        if(d == 1):
            value = data[d]
        elif(d == 2):
            change = sanitize(2, data[d])
        elif(d == 3):
            percentChange = sanitize(3, data[d])

    originalValue = calculateOriginalValue(value, change, percentChange)
    newEntriesInRecord.append(originalValue)
    newEntriesInRecord = "\t".join(newEntriesInRecord)
    newRecordsInFile.append(newEntriesInRecord)

print("Writing modified data to new file....")

f = open("modified-data.txt", "w")

for record in newRecordsInFile:
    f.write(record + "\n")

f.close()








