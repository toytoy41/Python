import json
import sys

from eliot import Message, start_action, to_file, write_traceback
import requests


# ログ出力を標準出力 (ターミナルにする)
to_file(sys.stdout)

# クロール対象のURLリスト
PAGE_URL_LIST = [
    'https://eliot.readthedocs.io/en/1.0.0/',
    'https://eliot.readthedocs.io/en/1.0.0/generating/index.html',
    'https://example.com/notfound.html',
]


def fetch_pages():
    """ページ内容を取得する."""
    # どの処理のログかをaction_typeで指定
    with start_action(action_type="fetch_pages"):
        page_contents = {}
        for page_url in PAGE_URL_LIST:
            # どの処理のログかをaction_typeで指定
            with start_action(action_type="download", url=page_url):
                try:
                    r = requests.get(page_url, timeout=30)
                    r.raise_for_status()
                except requests.exceptions.RequestException as e:
                    write_traceback()  # 例外時はトレースバックを出力する
                    continue
                page_contents[page_url] = r.text
        return page_contents


if __name__ == '__main__':
    page_contents = fetch_pages()
    with open('page_contents.json', 'w') as f_page_contents:
        json.dump(page_contents, f_page_contents, ensure_ascii=False)

    # 単純にログメッセージのみを出力することもできる
    Message.log(message_type="info", msg="クロールデータが保存されました.")
