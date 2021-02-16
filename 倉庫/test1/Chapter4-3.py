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

# データを保存する
cursor.execute("INSERT INTO books VALUES(%s, %s)", ("はじめてのPython", "https://example.com"))

# 変更をコミットする
connection.commit()

# 接続を閉じる
connection.close()
