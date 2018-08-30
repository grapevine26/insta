#-*- coding:utf-8 -*-

from selenium import webdriver
import re
import time
from bs4 import BeautifulSoup

def search(hashtag):
    # 크롤링할 주소
    url = 'https://www.instagram.com/explore/tags/'+hashtag
    # coreCount = 8 #스크롤할 양

    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(10)

    print("Searching "+url)

    # 스크롤내리는 횟수
    scrollCount = 2
    # URL 담을 딕셔너리
    URLtag = {}
    # 태그 URL 패턴.
    URLpattern = "(/p/)([0-9a-zA-Z|_|-]*)(/?)"
    # 패턴 컴파일
    URLre = re.compile(URLpattern)
    samecount = 0
    for i in range(0, scrollCount):
        # 페이지 전체 소스
        source = driver.page_source
        # 정규식 적용해서 리스트로 변환
        sourceURL = URLre.findall(source)
        # 튜플로 변함
        for URL in sourceURL:
            # URLtag {} 에 이미 같은 url이 있다면 중복
            if URL[1] in URLtag:
                print(URL[1] + '중복 URL')
                samecount += 1
            # dict에 url이 없다면 dict에 추가
            else:
                URLtag[URL[1]] = URL

        time.sleep(1)
        print("Scrolling... "+str(i+1)+"/"+str(scrollCount) + ", 현재: " + str(len(URLtag)) + ", 중복: " + str(samecount))
        # 스크롤
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # url이 저장된 dict와 사용하던 driver를 가지고 info 실행
    feed = info(URLtag, driver)
    print(feed)
    print(type(feed))
    return feed

def info(URLtag, driver):
    time.sleep(2)

    pageList = []

    # dict의 키값을 list에 추가
    for i in URLtag.keys():
        pageList.append(i)

    """for i in result1:
        pageList.append(i[1])"""

    print(str(len(pageList))+"개의 결과를 찾았습니다")

    counter = 1
    # pageList에 [URLtag] 들어있음
    for i in pageList:
        userURL = "https://www.instagram.com/p/" + i + "/"
        driver.get(userURL)
        driver.implicitly_wait(1)

        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')

        # 셀렉터를 이용해서 텍스트 가져오기
        # 게시물 본인 닉네임
        myname = driver.find_element_by_css_selector('#react-root > section > main > div > div > article > header > div.o-MQd > div.PQo_0 > div.e1e1d > a').text
        # 닉네임
        HTMLname = soup.select('#react-root > section > main > div > div > article > div.eo2As > div.KlCQn.EtaWk > ul > li > div > div > div > a')
        # 내용
        HTMLcontent = soup.select('#react-root > section > main > div > div > article > div.eo2As > div.KlCQn.EtaWk > ul > li > div > div > div > span')
        # 좋아요
        HTMLlike = soup.select('#react-root > section > main > div > div > article')
        # 이미지
        HTMLimage = soup.select('#react-root > section > main > div > div > article > div._97aPb.wKWK0 > div > div > div > div.tN4sQ.zRsZI > div > div.MreMs > div > ul > li:nth-of-type(1) > div > div > div > div.KL4Bh > img')
        if not HTMLimage:
            HTMLimage = soup.select('#react-root > section > main > div > div > article > div._97aPb.wKWK0 > div > div > div.KL4Bh > img')

        print(userURL)

        print('게시물닉네임 : '+myname)

        print('- 닉네임 - ')
        name = []
        for LISTname in HTMLname:
            name.append(LISTname.text)
        print(name)

        print('- 내용 -')
        content = []
        for LISTcontent in HTMLcontent:
            content.append(LISTcontent.text)
        print(content)

        print(' - 좋아요 - ')
        for LISTlikes in HTMLlike:
            likepattern= "(좋아요\s[0-9,]*개)"
            likere = re.compile(likepattern)
            like = likere.findall(LISTlikes.text)
            print(like)

        print(' - 이미지 -')
        for LISTimage in HTMLimage:
            image = LISTimage['src']
            print(image)

        print(str(counter)+" of "+str(len(pageList)))

        print("-"*100)
        counter += 1
    print("완료")
    return userURL, myname, name, content, like, image

if __name__ == '__main__':
    search('비키니')