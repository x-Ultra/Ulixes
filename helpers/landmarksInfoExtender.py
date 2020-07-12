import json
import base64
import requests
import csv
import os

image = False


# aggiungere versione nel DB, che viene caricata allo start up della macchina ulisse

def extractMonument(l):
    line = oldFileContent[l][:-1]
    return line.split(", ")[0]


def addDescriptionHeader():
    headerOld = oldFileContent[0][:-1]
    fn.write(headerOld)
    fn.write(", ")
    fn.write("Description")
    fn.write("\n")


def addPictureAndUrlHeader():
    headerOld = oldFileContent[0][:-1]
    fn.write(headerOld)
    fn.write(", ")
    fn.write("PictureUrl")
    fn.write("\n")


def appendOnFile(line, url):
    oldRaw = oldFileContent[line][:-1]
    fn.write(oldRaw)
    fn.write(", ")
    fn.write(url)
    fn.write("\n")


def appendDescription(line, desc):
    oldRaw = oldFileContent[line][:-1]
    fn.write(oldRaw)
    fn.write(", ")
    fn.write(desc)
    fn.write("\n")


def getImageOrDercription():
    if image:
        addPictureAndUrlHeader()
        searchType = "images"
    else:
        addDescriptionHeader()
        searchType = "web"

    for i in range(1, csvLines + 1):

        currentMonument = extractMonument(i)

        print("{}-> Searching {} for {}".format(i, searchType, currentMonument))

        r = requests.get("https://api.qwant.com/api/search/" + searchType,
                         params={
                             'count': 3,
                             'q': currentMonument,
                             't': searchType,
                             'safesearch': 1,
                             'uiv': 1,
                             'lenguage': "english"
                         },
                         headers={
                             'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
                             , "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3"
                         }
                         )

        response = r.json().get('data').get('result').get('items')

        if not image:
            sourceUrl = response[0]['source']
            sourceContent = response[0]['desc']

            completeDescription = '"' + sourceContent + '........Leggi di più su: ' + sourceUrl + '"'
            appendDescription(i, completeDescription)
        else:

            urls = [r.get('media') for r in response]
            try:
                firstImageLink = urls[0]
                img = base64.b64encode(requests.get(firstImageLink).content).decode("utf-8")
            except:
                print("Image NOT found")
                img = ""
                firstImageLink = ""

            appendOnFile(i, firstImageLink)

    fn.close()
    fo.close()


filenameOld = "fullMonumentInfo.csv"
fo = open(filenameOld, "r")

filenameNew = "landmarksComplete.csv"
fn = open(filenameNew, "a")

oldFileContent = fo.readlines()
fo.close()

csvLines = len(oldFileContent) - 1

getImageOrDercription()

