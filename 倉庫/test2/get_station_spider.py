# -*- encoding:utf-8 -*-

import json

from scrapy import Spider
from scrapy.http import Request


class GetStationSpider(Spider):
    name = "get_station_spider"
    allowed_domains = ["express.heartrails.com"]
    end_point = "http://geoapi.heartrails.com/api/json?method=getStations&postal=%s"

    custom_settings = {
        "DOWNLOAD_DELAY": 1.5,
    }

    # 郵便番号のリスト（本来はDBなどから取得する）
    postal_list = [
        1080072,
        1050013,
        1350063,
        1020072,
        9012206,
    ]

    # Spiderが起動したら、このメソッドが呼ばれる。APIをコールするためのリクエストを作成する。
    def start_requests(self):
        for postal in self.postal_list:
            url = self.end_point % postal
            yield Request(url, self.parse)

    # ダウンロード完了後に呼ばれるメソッド。レスポンスから情報を抽出し辞書形式で返す
    def parse(self, response):
        response = json.loads(response.body)
        result = response['response']['station'][0]

        yield {
            'postal': result["postal"],
            'name': result["name"],
            'line': result["line"],
            'latitude': result["y"],
            'longitude': result["x"],
            'prev': result['prev'],
            'next': result['next'],
        }