# # -*- coding: utf-8 -*-
# import sys
# from flask import Flask
# app = Flask(__name__)  # Flaskインスタンスの作成
#
# # トップページ / にアクセスした際に実行される関数
# @app.route("/")
# def hello():  # 関数名は任意
#     return "Hello World!"

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    name = "Hello World !!!"
    return name

@app.route('/good')
def good():
    name = "Good"
    return name

## おまじない
if __name__ == "__main__":
    app.run(debug=True)