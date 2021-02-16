import codecs

from selenium import webdriver

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import shutil
import urllib.request
from bs4 import BeautifulSoup
# from bs4 import Comment
# import lxml
import re
import codecs


WAIT_SECOND = 30

def Ranking(self):
    html = self.download()

    mainPrm = self.site['main']
    mainObj = BeautifulSoup(html, "lxml").find(mainPrm[0], {mainPrm[1]: mainPrm[2]})

    if True:
        # 　Style要素 削除
        obj2 = mainObj.find_all('style')

        for tmpPbj2 in obj2:
            tmpPbj2.decompose()

        # 　保存するのはデバッグ用
        tmpFile = 'decomposeFile.xml'
        with open(tmpFile, 'w') as foutTmp:
            foutTmp.write(mainObj.prettify(formatter='html'))

    rankingFile = 'ranking.txt'
    with open(rankingFile, 'wt') as fout:

        num = 1

        #   rank1から3、4から20までの処理
        i = 0
        for sub in self.site['sub']:
            itemParm = sub[0]
            obj3 = mainObj.find_all(itemParm[0], {itemParm[1]: itemParm[2]})
            # print (" ", parm[0], parm[1], parm[2], str(len(obj3)))

            for itemObjHtml in obj3:
                self.singleObj(itemObjHtml, sub[1], fout)

        # 　21位以下はJavaScript で書かれている。
        # 　別処理をしなければいけない。
        obj4 = mainObj.find_all('script', {'language': 'JavaScript'})
        # print(len(obj4))
        for sJavaObj in obj4:
            if sJavaObj.string is None:
                continue

            # JavaScriptでは、実データがコメント内に書かれているので、
            # コメントをdivタグに変えておく
            itemString = str(sJavaObj.string)
            # blockstring2 = blockstring.replace("<!--", "<div>").replace("-->", "</div>")
            re.sub('<!--', '<div>', itemString)
            re.sub('-->', '</div>', itemString)

            itemObj = BeautifulSoup(itemString, "lxml")
            self.singleObj(itemObj, self.site['sub'][1][1], fout)


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.maximize_window()
    # driver.get('https://www.amazon.co.jp/s/ref=nb_sb_noss?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Daps&field-keywords=%E3%83%A9%E3%83%B3%E3%82%AD%E3%83%B3%E3%82%B0&rh=i%3Aaps%2Ck%3A%E3%83%A9%E3%83%B3%E3%82%AD%E3%83%B3%E3%82%B0')
    # driver.get('https://www.amazon.co.jp/s/ref=nb_sb_noss?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Daps&field-keywords=%E3%83%A9%E3%83%B3%E3%82%AD%E3%83%B3%E3%82%B0&rh=i%3Aaps%2Ck%3A%E3%83%A9%E3%83%B3%E3%82%AD%E3%83%B3%E3%82%B0')
    # driver.get('https://ranking.rakuten.co.jp/?l-id=header_reco_search_1')   # 総合
    driver.get('https://ranking.rakuten.co.jp/daily/110983/?l2-id=ranking_a_top_gmenu')    #靴
    # driver.get('https://google.co.jp')

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

    obj = BeautifulSoup(driver.page_source, 'lxml')

    obj2 = obj.find_all('style')
    for tmpPbj2 in obj2:
        tmpPbj2.decompose()

    obj3 = obj.find_all('script')
    for tmpPbj3 in obj3:
        tmpPbj3.decompose()



    # 　保存するのはデバッグ用

    # print(obj)
    # ソースの書き出し
    # file_name = 'test.html'
    # with codecs.open(file_name, 'a', 'utf_8') as f:
    #     f.write(driver.page_source)
    file_name = 'test4.html'
    with codecs.open(file_name, 'a', 'utf_8') as f:
        f.write(obj.prettify())

    driver.close()