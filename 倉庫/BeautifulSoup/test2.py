#https://search.yahoo.co.jp/search;_ylt=A2Ri8AQAxHdaOkQA10yJBtF7?p=%E4%BD%8F%E5%AE%85%E3%83%AD%E3%83%BC%E3%83%B3%E3%81%8A%E3%81%99%E3%81%99%E3%82%81&search.x=1&fr=top_ga1_sa&tid=top_ga1_sa&ei=UTF-8&aq=-1&oq=%E4%BD%8F%E5%AE%85%E3%83%AD%E3%83%BC%E3%83%B3%E3%81%8A%E3%81%99%E3%81%99%E3%82%81&at=&aa=&ai=_tjt.e6CSp2VRbyxrrHtJA&ts=11585

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

# url = 'https://search.yahoo.co.jp/search;_ylt=A2Ri8AQAxHdaOkQA10yJBtF7?p=%E4%BD%8F%E5%AE%85%E3%83%AD%E3%83%BC%E3%83%B3%E3%81%8A%E3%81%99%E3%81%99%E3%82%81&search.x=1&fr=top_ga1_sa&tid=top_ga1_sa&ei=UTF-8&aq=-1&oq=%E4%BD%8F%E5%AE%85%E3%83%AD%E3%83%BC%E3%83%B3%E3%81%8A%E3%81%99%E3%81%99%E3%82%81&at=&aa=&ai=_tjt.e6CSp2VRbyxrrHtJA&ts=11585'
# url = 'https://search.yahoo.co.jp/search;_ylt=A2Ri8AQAxHdaOkQA10yJBtF7?p=住宅ローンおすすめ&search.x=1&fr=top_ga1_sa&tid=top_ga1_sa&ei=UTF-8&aq=-1&oq=住宅ローンおすすめ&at=&aa=&ai=_tjt.e6CSp2VRbyxrrHtJA&ts=11585'
#class="hb"
# url='https://www.amazon.co.jp/s/ref=nb_sb_noss_1?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Dstripbooks&field-keywords=python'
url='https://furukyo.matuba.org/'
# bsObj = BeautifulSoup(url, "lxml")
# print(bsObj)
#//*[@id="s-results-list-atf"]  //*[@id="atfResults"]
html = urlopen(url)
bsObj = BeautifulSoup(html, "lxml")
# print(bsObj)

# ランキング
attr='row widget-area'
# "widget-front"
obj2 = bsObj.find("div", {"class": attr})
print(obj2)

# pretyHtml = obj2.prettify()
#
# objXml = BeautifulSoup(pretyHtml, 'xml')
# objXml.findAll("div", class_="bd")
#
# print(pretyHtml)

#
# #　なぜか2行ある。このコード適当
# print("タイトル：" + cleanInput(ttle.get_text())[0]  + "\n")
#
# #　usrQstn　は二つある。
# obj2 = bsObj.findAll("div", {"class": "usrQstn"})[1]
# pretyHtml = obj2.prettify()
#
# objXml = BeautifulSoup(pretyHtml, 'xml')
# objXml.find("div", class_="attInf").decompose()
#
# # get_text()はリストを返す。
# str = "".join(cleanInput(objXml.get_text()))
# str = re.sub('[0-9]{4}/[0-9]{1,2}/[0-9]{4}:[0-9]{2}:[0-9]{2}', '', str)
#
# str2 = str.replace('さん', "さん\n").replace('。', "。\n", 50)
# # lst3=lst2.replace('。',"。\n",50)
# print("ベストアンサー：" + str2)
