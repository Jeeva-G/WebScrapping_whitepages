'''
Created on 23/05/2015

@author: jeevananthamganesan
'''
import csv
import requests
from bs4 import BeautifulSoup


def getdata(url):
    dic = {}
    r1 = requests.get(url)
    soup1 = BeautifulSoup(r1.content)
    g_data = soup1.find_all("div",{"class":"itemNameLocation"})
    for item in g_data:
        dic[item.contents[1].text] = [str(item.contents[3].text),str(item.contents[5].text)]
    return dic

def getdetails(eachname):
    #Looking only in Auckland region for now, it can be modified to look for any places.
    url = "https://whitepages.co.nz/white-all/"+str(eachname)+"/auckland-region/"
    newurl = url
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    pages = soup.find_all("h5",{"id":"searchResultsNumber"})
    if len(pages) > 0:
        for i in pages:
            test = i.text
            newtst = test.split("of ")
            new = (newtst[1])
            if new[-1:] != 's':
                out = 1
            else:
                out = int(new[0:-8])
        if out < 105:
            if(out < 106 and out > 90):
                urltime = 7
            elif(out < 91 and out > 75):
                urltime = 6
            elif(out < 76 and out > 60):
                urltime = 5
            elif(out < 61 and out > 45):
                urltime = 4
            elif(out < 46 and out > 30):
                urltime = 3
            elif(out < 31 and out > 15):
                urltime = 2
            elif(out < 16):
                urltime = 1
        else:
            urltime = 8

        outputdic = []
        for i in range(urltime):
            i = i+1
            urls = newurl+str(i)+"/"
            output = getdata(urls)
            for j in output:
                outputdic.append(output[j])
        return(outputdic)



if __name__ == '__main__':
    #Getting the input and output file paths
    InputFilepath = sys.argv[1]
    OutputFilepath = sys.argv[2]
    with open(InputFile, 'rU') as f:
        reader = csv.reader(f)
        inputval = list(reader)
        input_list = [y for x in inputval for y in x]

    for eachname in input_list:
        outputdata = getdetails(eachname)
        if outputdata is not None:
            with open(OutputFilepath, "a") as f:
                writer = csv.writer(f)
                writer.writerows(outputdata)
