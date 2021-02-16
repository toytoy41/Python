from urllib.request import urlopen
from bs4 import BeautifulSoup
import lxml
import re
import string
from collections import OrderedDict

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
# soup = BeautifulSoup(html_doc, "html.parser")  #, 'lxml')
#
# for link in soup.find_all('a'):
#     print(link.get('href'))
#
# print(soup.prettify())
#
# print(soup.get_text())

# html = urlopen('https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11183286981?__ysp=44Kr44Oh44OpIOS6uuawlw%3D%3D')
# soup = BeautifulSoup('https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11183286981?__ysp=44Kr44Oh44OpIOS6uuawlw%3D%3D') #, 'lxml')
# bsobj = BeautifulSoup(html, 'lxml')
# tag = bsobj.find(id='contents')
# print(tag)
# print(tag.get_text())

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

# xml_soup = BeautifulSoup('https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11183286981?__ysp=44Kr44Oh44OpIOS6uuawlw%3D%3D', 'html.parser')
url= 'https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11183286981'
html = urlopen(url)
bsObj = BeautifulSoup(html, "lxml") #""html.parser")

# pobj = bsObj.prettify()
# print(pobj)

obj2 = bsObj.find("div", {"class": "ptsQes"})
print(obj2.get_text())

objXml = obj2.prettify()
print(objXml)

obj3 = BeautifulSoup(objXml,'lxml')
print(obj3)
# print(obj3.get_text())

# obj3= obj2.div.decompose()
# print(obj3)
# content=obj3.find("div", {"class": "ptsQes"}).get_text()

# ngrams = cleanInput(obj3)

# ngrams = OrderedDict(sorted(ngrams.items(), key=lambda t: t[1], reverse=True))
# print(ngrams)

# print("タイトル：" + bsObj.find("div", {"class": "ttl"}).get_text())
# print("ベストアンサー：" + bsObj.find("div", {"class": "ptsQes"}).get_text())

# obj1 =xml_soup.find( id="contents")
# obj1 = xml_soup.find("div", class_="ttl")
# XPATH は使えない
# obj1 =xml_soup.find( '//div[@class="ptsQes"]')
# //*[@id="main"]/div[1]/div[1]/h1
# //*[@id="main"]/div[1]/div[3]/div[2]/div[2]/p[1]/text()[1]

# obj1 = xml_soup.find("div", {"cladd":"ptsQes"})
# print(bsObj)

# //*[@id="main"]/div[3]/div[1]/h2

# tag2 = tag['main']
# print(tag2)
# print( bsobj.find(id='contents').find(['ttl'])) #.find(['ttl']))

# print( bsobj.find(class="postQes").find(".get_text())

# tag = soup.h2
#
# # type(tag)
#
# #print(type(tag))
# print(tag.get_text())
# print (tag['class'])

# print (tag.attrs)

# print(tag['class'])
#
# xml_soup = BeautifulSoup('<p class="body strikeout"></p>', 'xml')
# aaa = xml_soup.p['class']
# print (aaa) # u'body strikeout')
#
# tag.string
# print (tag.string)
# # u'Extremely bold'
# type(tag.string)
# # <class 'bs4.element.NavigableString'>