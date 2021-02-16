import json
import time

import requests

# クロールするURLリスト
PAGE_URL_LIST = [
    'http://example.com/1.page',
    'http://example.com/2.page',
    'http://example.com/3.page',
]


def fetch_pages():
    """ページ内容を取得する."""
    # 処理経過を記録するログファイルを追記モードで開く
    f_info_log = open('crawler_info.log', 'a')
    # エラーを記録するログファイルを追記モードで開く
    f_error_log = open('crawler_error.log', 'a')

    # 取得内容を保存するための辞書型変数
    page_contents = {}

    # ターミナルへの処理の開始を表示し、ログファイルにも同じメッセージを書き出す
    msg = "クロールを開始します\n"
    print(msg)
    f_info_log.write(msg)

    for page_url in PAGE_URL_LIST:
        r = requests.get(page_url, timeout=30)
        try:
            r.raise_for_status()  # 応答が異常の場合は例外エラーを発生させる
        except requests.exceptions.RequestException as e:
            # requestsの例外エラーが発生した場合は、
            # ターミナルとエラーログにエラーを出力する
            msg = "[ERROR] {exception}\n".format(exception=e)
            print(msg)
            f_error_log.write(msg)
            continue  # 例外時はループを中断せずスキップする

        # 正常に内容が取得できたら辞書型変数に取得内容を保存する
        page_contents[page_url] = r.text
        time.sleep(1)  # 相手サイトへの負荷を考慮しリクエストの間隔を空ける

    f_info_log.close()
    f_error_log.close()
    return page_contents


if __name__ == '__main__':
    page_contents = fetch_pages()
    f_page_contents = open('page_contents.json', 'w')
    json.dump(page_contents, f_page_contents, ensure_ascii=False)
    f_page_contents.close()
