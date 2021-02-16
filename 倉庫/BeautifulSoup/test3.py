from urllib.request import urlopen
from bs4 import BeautifulSoup
import lxml

import re
import string

def cleanInput(input):
    input = re.sub('\n+', " ", input)
    input = re.sub('\t+', " ", input)
    # input = re.sub('\[[0-9]*\]', "", input)
    input = re.sub(' +', " ", input)
    # input = bytes(input, "UTF-8")
    # input = input.decode("ascii", "ignore")
    cleanInput = []
    input = input.split(' ')
    for item in input:
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            cleanInput.append(item)
    return cleanInput

def getNgrams(input, n):
    input = cleanInput(input)
    output = dict()
    for i in range(len(input)-n+1):
        newNGram = " ".join(input[i:i+n])
        if newNGram in output:
            output[newNGram] += 1
        else:
            output[newNGram] = 1
    return output

url= 'https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11183286981'
# url = 'https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q10184505960?__ysp=44OH44K444Kr44Oh'

html = urlopen(url)
bsObj = BeautifulSoup(html, "lxml")

# ttle = bsObj.findAll("div", {"class": "usrQstn"})
print(bsObj.findAll("div", {"class": "usrQstn"})[1].get_text())
print(bsObj.findAll("div", {"class": "ptsQes"})[1].get_text())
