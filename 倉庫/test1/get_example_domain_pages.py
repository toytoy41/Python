import time

import requests

PAGE_URL_LIST = [
    'http://example.com/1.page',
    'http://example.com/2.page',
    'http://example.com/3.page',
]

for page_url in PAGE_URL_LIST:
    res = requests.get(page_url, timeout=30)
    print(
        "ページURL: " + page_url + ", " + \
        "HTTPステータス: " + str(res.status_code) + ", " + \
        "処理時間(秒): " + str(res.elapsed.total_seconds())
    )
    time.sleep(1)
