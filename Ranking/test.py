import codecs

from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import shutil
from urllib.request import urlopen, request_host
import urllib.request
from bs4 import BeautifulSoup
# from bs4 import Comment
# import lxml
import re
import codecs


WAIT_SECOND = 30
SITE楽天総合ランキング = {
    '楽天総合' : {'url' : 'https://ranking.rakuten.co.jp/?l-id=header_reco_search_1',
              'main' : ['div','id','rnkRankingMain'],
              'sub' : [[['dl','class','rnkRanking_top3box'],['dt','class','rnkTop_itemName']],
                       [['dl','class','rnkRanking_after4box'],['dt','class','rnkTop_itemName']]]}
}

SITE紳士靴ランキング = {
    '紳士靴' : {'url' : 'https://ranking.rakuten.co.jp/daily/110983/?l2-id=ranking_a_top_gmenu',
              'main' : ['div','id','rnkRankingMain'],
              'sub': [[['div', 'class', 'rnkRanking_top3box'],['div','class','rnkRanking_detail']],
                      [['div', 'class', 'rnkRanking_after4box'],['div','class','rnkRanking_detail']]]}
}

SITEドレスランキング = {
    'ドレス' : {'url' : 'https://ranking.rakuten.co.jp/daily/555084/?l2-id=ranking_a_top_gmenu',
              'main' : ['div','id','rnkRankingMain'],
              'sub' : [[['div','class','rnkRanking_top3box'],['div','class','rnkRanking_detail']],
                       [['div','class','rnkRanking_after4box'],['div','class','rnkRanking_detail']]]}
}

SITES={}
SITES.update(SITE楽天総合ランキング)
SITES.update(SITE紳士靴ランキング)
SITES.update(SITEドレスランキング)

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.maximize_window()
    # driver.get('https://www.amazon.co.jp/s/ref=nb_sb_noss?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Daps&field-keywords=%E3%83%A9%E3%83%B3%E3%82%AD%E3%83%B3%E3%82%B0&rh=i%3Aaps%2Ck%3A%E3%83%A9%E3%83%B3%E3%82%AD%E3%83%B3%E3%82%B0')
    # driver.get('https://www.amazon.co.jp/s/ref=nb_sb_noss?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Daps&field-keywords=%E3%83%A9%E3%83%B3%E3%82%AD%E3%83%B3%E3%82%B0&rh=i%3Aaps%2Ck%3A%E3%83%A9%E3%83%B3%E3%82%AD%E3%83%B3%E3%82%B0')
    # driver.get('https://ranking.rakuten.co.jp/?l-id=header_reco_search_1')   # 総合
    driver.get('https://ranking.rakuten.co.jp/daily/110983/?l2-id=ranking_a_top_gmenu')    #靴
    # driver.get('https://google.co.jp')
    driver.find_element_by_tag_name("html")

    # 検索キーワードとエンターキーを入力
    # t = driver.find_element_by_id('lst-ib')
    # t.send_keys(u'てけとーぶろぐ\n')

    # 要素の表示待ち
    # WebDriverWait(driver, WAIT_SECOND).until(
    #     EC.visibility_of_element_located((By.CLASS_NAME, '_Rm')))
    #
    # # リンクをクリック
    # b = driver.find_element_by_xpath('//*[@id="rso"]/div/div/div[1]/div/div/h3/a')
    # b.click()
    #
    # 要素の表示待ち
    # WebDriverWait(driver, WAIT_SECOND).until(
    #     EC.visibility_of_element_located((By.CLASS_NAME, 'entry-title-link')))

    # mainObj = BeautifulSoup(driver.page_source, 'lxml')

    file_name = 'test5.html'
    with codecs.open(file_name, 'a', 'utf_8') as f:
        f.write(driver.page_source())
        # f.write(mainObj.prettify())

    driver.close()

    # site = SITES['楽天総合']
    # sub1 = site['sub'][0][0]
    #
    # obj3 = mainObj.find_all(sub1[0], {sub1[1]: sub1[2]})
    # # print(len(obj3))
    #
    # sub2 = site['sub'][1][0]
    # obj4 = mainObj.find_all(sub2[0], {sub2[1]: sub2[2]})
    # print(len(obj4))


    # obj2 = obj.find_all('style')
    # for tmpPbj2 in obj2:
    #     tmpPbj2.decompose()
    #
    # obj3 = obj.find_all('script')
    # for tmpPbj3 in obj3:
    #     tmpPbj3.decompose()


    # 　保存するのはデバッグ用

    # print(obj)
    # ソースの書き出し
    # file_name = 'test.html'
    # with codecs.open(file_name, 'a', 'utf_8') as f:
    #     f.write(driver.page_source)
