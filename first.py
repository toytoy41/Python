# print("Hello World!")
# import sys
# for place in sys.path:
#    print(place)
#wget 'hhtps://www.nak.co.jp/'
import feedparser
import MySQLdb
#import mysqlclient
connection = MySQLdb.connect(
    user = "scrapingman",
    password = "myPassword-1",
    host = "localhost",
    db = "scrapingdata",
    charset = "utf8"
)
type(connection)
#cursor = connection.cursor()

# カーソルを生成する
cursor = connection.cursor()
type(cursor)

# 実行する度に同じ結果になるようにテーブルを削除しておく
cursor.execute("DROP TABLE IF EXISTS books")

# テーブルを作成する
cursor.execute("CREATE TABLE books (title text, url text)")

# データを保存する
cursor.execute("INSERT INTO books VALUES(%s, %s)", ("はじめてのPython", "https://example.com"))

# 変更をコミットする
connection.commit()

# 接続を閉じる
connection.close()


"""
import feedparser
rss = feedparser.parse("http://www.shoeisha.co.jp/rss/index.xml")
print(rss)
print(rss{"feed"})
print(rss["feed"]["title"])
#*********************
import requests
import lxml.html
#r = requests.get("http://waether.livedoor.com/weather_hacks/webservice")
#r = requests.get("http://weather.livedoor.com/forecast/webservice/json/v1")
#r = requests.get("http://weather.livedoor.com/forecast/webservice/json/v1?city=400040")
r = requests.get("http://www.shoeisha.co.jp/book/detail/9784798146072")
html = r.text
#print(html)
root = lxml.html.fromstring(html)
print(root)
titleH1 = root.xpath("/html/body/div[1]/section/h1")
print(titleH1)
print(titleH1[0].text)
qaA = root.cssselect("#qa > p > a")
for aTag in qaA:
    print(aTag.attrib["href"])


"""
#print(r.text)
#r = requests.get("http://www.drk7.jp/weather/xml/12.xml")
#r.status_code
#myjson = r.json()
#print(myjson["description"]["text"])

'''
class Duck():
    def __init__(self, input_name):
        self.__name = input_name

    @property
    def name(self):
        print('inside the getter')
        return self.__name

    @name.setter
    def name(self, input_name):
        print('inside the setter')
        self.__name = input_name


fowl = Duck('Howard')
fowl.name
print(fowl._Duck__name)
'''
