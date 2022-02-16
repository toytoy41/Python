#https://www.amazon.co.jp/gp/product/B004VPVTIC/ref=s9_acsd_ps_hd_bw_b4plL9_c_x_1_w?pf_rd_m=AN1VRQENFRJN5&pf_rd_s=merchandised-search-8&pf_rd_r=J6YQDN7S96BEMK5KHXTZ&pf_rd_t=101&pf_rd_p=a90f53b1-2340-5be9-a07e-528c94c61c18&pf_rd_i=71442051
import codecs
import shutil
import sys
import time
import urllib.request
from urllib.request import urlopen  # , request_host

from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver

# from beautifulsoup4 import BeautifulSoup

WAIT_SECOND = 30
RES_OUT = 'Res\\'

class Rank():
    def __init__(self, site):
        '''
        :param site:
        '''
        self.site=site
        self.num = 1

    def download(self):
        '''  一度ファイルに保存しないと情報が得られない。 '''

        html =''

        if True:

            driver = webdriver.Chrome()
            driver.get(self.site['url'])

            try:
                # time.sleep(WAIT_SECOND)
                # html = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"loaddedButton")))

                if False:
                    last_check = self.site['sub'][1][0][2]
                    print(last_check)
                else:
                    last_check = 'rnkRanking_after4box'

                WebDriverWait(driver, WAIT_SECOND).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, last_check)))
                html = driver.page_source.encode('utf-8')

            finally:
                driver.close()

        else:
            tmpFile = 'temp.html'
            urllib.request.urlretrieve(self.site['url'], "{0}".format(tmpFile))

            html = ''
            with  codecs.open(tmpFile, 'r', 'utf-8') as file:
                html = file.read()

        return html


    def Ranking(self):

        html = self.download()
        mainPrm = self.site['main']
        mainObj = BeautifulSoup(html, "lxml").find(mainPrm[0],{mainPrm[1]:mainPrm[2]})

        # print(mainObj.prettify())
        if True:
            # 　Style要素 削除
            obj2 = mainObj.find_all('style')
            for tmpPbj2 in obj2:
                tmpPbj2.decompose()

            # Script要素　削除
            obj1 = mainObj.find_all('script')
            for tmpPbj2 in obj1:
                tmpPbj2.decompose()

            #　保存するのはデバッグ用
            tmpFile = RES_OUT +  'decomposeFile.xml'
            with open(tmpFile, 'w') as foutTmp:
                foutTmp.write(mainObj.prettify(formatter='html'))

        rankingFile = RES_OUT + 'ranking.txt'
        with open(rankingFile, 'wt') as fout:

            num = 1

            #   rank1から3、4から20までの処理
            i = 0
            for sub in self.site['sub']:
                itemParm = sub[0]
                obj3 = mainObj.find_all(itemParm[0], {itemParm[1]: itemParm[2]})
                # print(len(obj3))

                for itemObj in obj3:
                    # self.singleObj(itemObjHtml, sub[1], fout)
                    # singleObj2(self, itemObj, detailPrm, fout):

                    detailPrm = sub[1]
                    detailObj = itemObj.find(detailPrm[0], {detailPrm[1]: detailPrm[2]})

                    if detailObj is None:
                        # print('None ;')
                        return None

                    rank = str(self.num) + "位　"
                    self.num += 1
                    title = rank + detailObj.find('a').string
                    lnkURL = detailObj.a.attrs['href']

                    if True:
                        fout.write(title + '\n')
                        # fout.write('\n')
                        # fout.write("　　" + str(lnk))
                        fout.write("\t" + str(lnkURL + '\n'))
                        # fout.write('\n')
                    else:
                        print(title)
                        print(lnkURL)


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

def go(siteName):
    rank1 = Rank(SITES[siteName])

    rank1.Ranking()
    shutil.copy( RES_OUT + 'ranking.txt',  RES_OUT + siteName + 'rannking.txt')
    shutil.copy( RES_OUT + 'decomposeFile.xml',  RES_OUT + siteName + 'decomposeFile.txt')

if __name__ == '__main__':

    # go('楽天総合')
    # go('紳士靴')
    go('ドレス')

    #     # output
    #     output = {"title": title, "description": description_content}
    #     # write the output as a json file
    #     with codecs.open(output_name, 'w', 'utf-8') as fout:
    #         json.dump(output, fout, indent=4, sort_keys=True, ensure_ascii=False)
    #

    sys.exit()
