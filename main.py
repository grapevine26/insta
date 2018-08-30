# from selenium import webdriver
# from bs4 import BeautifulSoup
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setting.settings')
# import django
# django.setup()
# from crawling.models import *
# from selenium.webdriver.common.keys import Keys
# import time
#
# def parse_blog():
#     url = "https://www.instagram.com/1.7.1/?hl=ko"
#     driver = webdriver.Chrome()
#     driver.implicitly_wait(3)
#     driver.get(url)
#     elem = driver.find_element_by_tag_name("body")
#     # 이미지 url
#     imgURL = driver.find_element_by_css_selector('header > div > div > span > img').get_attribute('src')
#     # 닉네임
#     name = driver.find_element_by_css_selector('div.nZSzR > h1').text
#     # 팔로워
#     follower = driver.find_element_by_css_selector("li:nth-child(2) > a > span").text
#     print("imgURL : " + imgURL)
#     print("name : " + name)
#     print("follower : " + follower)
#     page_down = 0
#     data = []
#     # 내용
#     while page_down < 1:
#         elem.send_keys(Keys.PAGE_DOWN)
#         time.sleep(1)
#         print('크롤링 시작')
#         my_titles = driver.find_elements_by_css_selector('div.KL4Bh > img')
#         for title in my_titles:
#             if not title.get_attribute('alt') in data:
#                 re = title.get_attribute('alt').replace(".", "").replace("\n", "").replace("️", "").replace("✔️", "")
#                 data.append('『'+re+'』')
#         page_down += 1
#
#
#     return imgURL, name, follower, data
#
# if __name__ == '__main__':
#     u, x, y, z = parse_blog()
#     insta(imgURL=u, name=x, follower=y, content=z).save()
#
#
# '''
# # python 파일 위치
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#
# req = request.get('https://beomi.github.io/beomi.github.io_old/')
# html = req.text
# soup = BeautifulSoup(html, 'html.parser')
# my_titles = soup.select(
#     'h3 > a'
# )
#
# data = {}
#
# for title in my_titles:
#     data[title.text] = title.get('href')
#
# with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
#     json.dump(data, json_file)
# '''
#-*- coding:utf-8 -*-

from selenium import webdriver
import re
import time
from bs4 import BeautifulSoup
import urllib.request

def search(hashtag):
    # 크롤링할 주소
    url = 'https://www.instagram.com/explore/tags/'+hashtag
    #coreCount = 8 #스크롤할 양

    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(10)

    print("Searching "+url)

    #스크롤내리는 횟수
    scrollCount = 2
    dictionary = {}
    # 태그 리스트 주소 추출.
    mainPattern = "(/p/)([0-9a-zA-Z|_|-]*)(/?)"
    mainRegex = re.compile(mainPattern)
    samecount = 0
    for i in range(0, scrollCount):
        # 페이지 전체 소스
        source = driver.page_source
        # 정규식 적용해서 리스트로 변환
        search = mainRegex.findall(source)
        # 튜플로 변함
        for mainAdder in search:
            # dict에 이미 같은 url이 있다면
            if mainAdder[1] in dictionary:
                print(mainAdder[1] + '중복 URL')
                samecount += 1
            else:
                # dict에 url이 없다면 dict에 추가
                dictionary[mainAdder[1]] = mainAdder

        time.sleep(1)
        print("Scrolling... "+str(i+1)+"/"+str(scrollCount) + ", 현재: " + str(len(dictionary)) + ", 중복: " + str(samecount))
        # 스크롤
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # url이 저장된 dict와 사용하던 driver를 가지고 info 실행
    info(dictionary, driver)

def info(dictionary, driver):
    time.sleep(2)

    pageList = []

    # dict의 키값을 list에 추가
    for i in dictionary.keys():
        pageList.append(i)

    """for i in result1:
        pageList.append(i[1])"""

    print(str(len(pageList))+"개의 결과를 찾았습니다.n")

    # 사진 url 찾는 정규식
    pattern2 = '(display_url":")([0-9a-zA-Z]*://[0-9a-zA-Z|_|.|/|-]*)(")'
    regexp2 = re.compile(pattern2)

    counter = 1
    allCounter = 0
    # pageList [url] 들어있음
    for i in pageList:
        userURL = "https://www.instagram.com/p/" + i + "/"
        driver.get(userURL)
        driver.implicitly_wait(1)

        source2 = driver.page_source
        soup = BeautifulSoup(source2, 'html.parser')
        result2 = regexp2.findall(source2)

        # 셀렉터를 이용해서 텍스트 가져오기
        # 닉네임
        name = driver.find_element_by_css_selector('#react-root > section > main > div > div > article > header > div.o-MQd > div.PQo_0 > div.e1e1d > a').text
        # 본문
        HTMLcontent = soup.select('#react-root > section > main > div > div > article > div.eo2As > div.KlCQn.EtaWk > ul > li:nth-of-type(1) > div > div > div > span')
        # 본문태그
        HTMLtag1 = soup.select('#react-root > section > main > div > div > article > div.eo2As > div.KlCQn.EtaWk > ul > li:nth-of-type(1) > div > div > div > span > a')
        # 댓글태그
        HTMLtag2 = soup.select('#react-root > section > main > div > div > article > div.eo2As > div.KlCQn.EtaWk > ul > li:nth-of-type(2) > div > div > div > span > a')
        # 댓글
        HTMLreply = soup.select('#react-root > section > main > div > div > article > div.eo2As > div.KlCQn.EtaWk > ul > li > div > div > div ')
        # 좋아요
        HTMLlike = soup.select('#react-root > section > main > div > div > article')
        print('이름 : '+name)

        # driver.find 는 webelement 객체라서 정규식패턴이 적용안댐
        # soup.select는 리스트객체라서 for문으로 돌린다음 정규식 적용
        print('- 본문 - ')
        for LISTcontent in HTMLcontent:
            # contentpattern = "[^#]+"
            # contentre = re.compile(contentpattern)
            # content = contentre.findall(LISTcontent.text)
            # print(content[0])
            print(LISTcontent.text)

        print('- 본문태그 - ')
        for LISTtag1 in HTMLtag1:
            # tagPattern1 = "(#[0-9a-zA-Z가-힣ㄱ-ㅎ]+[^댓글])"
            # tagre1 = re.compile(tagPattern1)
            # tag1 = tagre1.findall(LISTtag1.text)
            # print(tag1)
            print(LISTtag1.text)

        print('- 댓글태그 - ')
        for LISTtag2 in HTMLtag2:
            # tagPattern2 = "(#[0-9a-zA-Z가-힣ㄱ-ㅎ]+[^#])"
            # tagre2 = re.compile(tagPattern2)
            # tag2 = tagre2.findall(LISTtag2.text)
            # print(tag2)
            print(LISTtag2.text)

        print('- 댓글 -')
        for LISTreply in HTMLreply:
            print(LISTreply.text)

        print(' - 좋아요 - ')
        for LISTlikes in HTMLlike:
            likepattern= "(좋아요\s[0-9,]*개)"
            likere = re.compile(likepattern)
            like = likere.findall(LISTlikes.text)
            print(like)

        print(str(counter)+" of "+str(len(pageList)))
        print(userURL+", "+str(len(result2))+"개의 이미지")
        # 이미지 다운로드
        # downloadCounter = 1
        # for downloadUrl in result2:
        #     print(downloadUrl)
        #     dirTemp = "C:picture" + i + "_" + str(downloadCounter).zfill(4) + ".jpg"
        #     print(dirTemp)
        #     urllib.request.urlretrieve(downloadUrl[1], dirTemp)
        #     downloadCounter +=
        # 1
        #     allCounter += 1

        print("-"*100)
        counter += 1
    print("완료")
    #print("총 "+str(allCounter)+"개의 사진을 다운로드했습니다.")

if __name__ == '__main__':
    search('비키니')