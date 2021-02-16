import feedparser

# URLを指定してFeedParserDictオブジェクトを取得する
rss = feedparser.parse("http://www.shoeisha.co.jp/rss/index.xml")

# RSSのバージョンを取得する
print(rss.version)

# フィードのタイトルとコンテンツの発行日時を表示する
print(rss["feed"]["title"])
print(rss["feed"]["published"])

# 各エントリーのタイトルとリンクを表示する
for content in rss["entries"]:
    print(content["title"])
    print(content["link"])
