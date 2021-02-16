import feedparser
import MySQLdb 

# データベースに接続する
connection = MySQLdb.connect(
  user="scrapingman",
  passwd="myPassword-1",
  host="localhost",
  db="scrapingdata",
  charset="utf8")

# カーソルを生成する
cursor = connection.cursor()

# 実行する度に同じ結果になるようにテーブルを削除しておく
cursor.execute("DROP TABLE IF EXISTS books")

# テーブルを作成する
cursor.execute("CREATE TABLE books (title text, url text)") 

# URLを指定してFeedParserDictオブジェクトを取得する
rss = feedparser.parse("http://www.shoeisha.co.jp/rss/index.xml")

# RSSのバージョンを取得する
print(rss.version)

# フィードのタイトルとコンテンツの発行日時を表示する
print(rss["feed"]["title"])
print(rss["feed"]["published"])

# 各エントリーのタイトルとリンクを表示する
for content in rss["entries"]:
    # データを保存する
    cursor.execute("INSERT INTO books VALUES(%s, %s)", (content["title"], content["link"])) 

# 変更をコミットする 
connection.commit()

# 接続を閉じる
connection.close() 