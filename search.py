#-*- coding:utf-8 -*-

from selenium import webdriver
import time
import re
from bs4 import BeautifulSoup

def searchCrawling(hashtag):
    # 크롤링할 주소
    url = 'https://www.instagram.com/explore/tags/'+hashtag

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    driver.implicitly_wait(3)
    driver.get_screenshot_as_file('search_headless.png')

    print("Searching "+url)

    # 스크롤내리는 횟수
    scrollCount = 4
    # 중복횟수
    samecount = 0

    for i in range(0, scrollCount):
        # 페이지 전체 소스
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        contentHTML = soup.select('div.eLAPa > div.KL4Bh > img')

        contentDICT = {}
        for contentLIST in contentHTML:
            try:
                if contentLIST['alt'] in contentDICT:
                    print(contentLIST['alt'] + '중복')
                    samecount += 1
                else:
                    hrefDICT = {}
                    mainPattern = "(/p/)([0-9a-zA-Z|_|-]*)(/?)"
                    mainRegex = re.compile(mainPattern)
                    content = mainRegex.findall(contentLIST.find_parent('a')['href'])
                    hrefDICT[content[0][1]] = contentLIST['src']
                    contentDICT[contentLIST['alt']] = hrefDICT
                    print('-'*50)
            except KeyError:
                pass
        # list=['a', 'b', 'c', 'd']
        # dictA = {}
        #
        # for list_ in list:
        #     dictB = {}
        #     dictB[list_] = list_
        #     dictA[list_] = dictB
        # print(dictA)
        print(contentDICT)
        time.sleep(1)
        print("Scrolling... "+str(i+1)+"/"+str(scrollCount) + ", 현재: " + str(len(contentDICT)) + ", 중복: " + str(samecount))
        # 스크롤
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    return contentDICT
