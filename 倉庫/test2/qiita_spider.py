# import scrapy
#
#
# class QiitaSpider(scrapy.Spider):
#     name = 'qiita_spider'
#
#     # エンドポイント（クローリングを開始するURLを記載する）
#     start_urls = ['http://qiita.com/advent-calendar/2015/categories/programming_languages']
#
#     custom_settings = {
#         "DOWNLOAD_DELAY": 1,
#     }
#
#     # URLの抽出処理を記載
#     def parse(self, response):
#         for href in response.css('.adventCalendarList .adventCalendarList_calendarTitle > a::attr(href)'):
#             full_url = response.urljoin(href.extract())
#
#             # 抽出したURLを元にRequestを作成し、ダウンロードする
#             yield scrapy.Request(full_url, callback=self.parse_item)
#
#     # ダウンロードしたページを元に、内容を抽出し保存するItemを作成
#     def parse_item(self, response):
#
#         urls = []
#         for href in response.css('.adventCalendarItem_entry > a::attr(href)'):
#             full_url = response.urljoin(href.extract())
#             urls.append(full_url)
#
#         yield {
#             'title': response.css('h1::text').extract(),
#             'urls': urls,
#         }
import scrapy


class QuotesSpider(scrapy.Spider):
    # name = "qiita_spider"
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)