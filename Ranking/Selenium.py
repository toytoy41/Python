import time
from bs4 import BeautifulSoup
import sys
import json

from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import codecs

WAIT_SECOND = 30

try:

    driver = webdriver.Chrome()
    # driver = webdriver.Chrome(executable_path=r'E:\Python\Selenium')
    # driver = webdriver.PhantomJS(executable_path='') #E:\Python\Seleium
    # driver = webdriver.Chrome(executable_path=r"C:\Users\Toyotoshi\AppData\Roaming\Python\Python36\site-packages\selenium\webdriver\chrome")
    # driver = webdriver.Chrome(executable_path='C:\\Users\\Toyotoshi\\AppData\\Roaming\\Python\\Python36\\site-packages\\selenium\\webdriver\\chrome')
    # driver.get('https://ranking.rakuten.co.jp/?l-id=header_reco_search_1')
    driver.get('https://www.amazon.co.jp/s/ref=nb_sb_noss?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Daps&field-keywords=%E3%83%A9%E3%83%B3%E3%82%AD%E3%83%B3%E3%82%B0&rh=i%3Aaps%2Ck%3A%E3%83%A9%E3%83%B3%E3%82%AD%E3%83%B3%E3%82%B0')
    html = driver.page_source.encode('utf-8')

    time.sleep(3)
    # items = driver.find_element_by_id("rnkRankingMain")
    soup = BeautifulSoup(driver.page_source,"lxml")
    header = soup.find("head")
    title = header.find("title").text

    # driver.find_element_by_tag_name("html")
    #
    # print(obj.body)

    # output
    output = {"title": title, "description": description_content}
    # write the output as a json file
    # with codecs.open(output_name, 'w', 'utf-8') as fout:
    #     json.dump(output, fout, indent=4, sort_keys=True, ensure_ascii=False)

    file_name = 'test.html'
    with codecs.open(file_name, 'a', 'utf_8') as f:
        f.write(driver.page_source)

    # print(obj.prettify())
    # print(driver.page_source)
    driver.close()

except Exception as ex:
    print("Exception :  : ", ex)
finally:
    pass

