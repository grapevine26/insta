#-*- coding:utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
from search import searchCrawling
import re
import time
import random

def detailCrawling(URLtag):
    time.sleep(2)
    userURL = "https://www.instagram.com/p/" + URLtag + "/"

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome(chrome_options=options)
    driver.get(userURL)
    driver.implicitly_wait(3)
    driver.get_screenshot_as_file('detail_headless.png')

    pageList = []
    counter = 1

    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')

    # 본인 닉네임
    HTMLnames = soup.select('#react-root > section > main > div > div > article > header > div.o-MQd > div.PQo_0 > div.e1e1d > a')
    # 내용
    HTMLcontent = soup.select('#react-root > section > main > div > div > article > div.eo2As > div.KlCQn.EtaWk > ul > li > div > div > div')
    # 좋아요
    HTMLlike = soup.select('#react-root > section > main > div > div > article')
    # 이미지
    HTMLimage = soup.select('#react-root > section > main > div > div > article > div._97aPb.wKWK0 > div > div > div > div.tN4sQ.zRsZI > div > div.MreMs > div > ul > li:nth-of-type(1) > div > div > div > div.KL4Bh > img')
    if not HTMLimage:
        HTMLimage = soup.select('#react-root > section > main > div > div > article > div._97aPb.wKWK0 > div > div > div.KL4Bh > img')

    print(userURL)
    print('- 게시물 닉네임 - ')
    for LISTnames in HTMLnames:
        names = LISTnames.text
    print(LISTnames.text)

    print('- 내용 -')
    content = {}
    for LISTcontent in HTMLcontent:
        content[LISTcontent.next.text] = LISTcontent.find_next('span').text
    print(content)

    print(' - 좋아요 - ')
    for LISTlikes in HTMLlike:
        likepattern= "(좋아요\s[0-9,]*개)"
        likere = re.compile(likepattern)
        likes = likere.findall(LISTlikes.text)
        like = ''.join(likes)
        print(like)

    print(' - 이미지 -')
    global image
    for LISTimage in HTMLimage:
        image = LISTimage['src']
        print(image)

    print(str(counter)+" of "+str(len(pageList)))

    print("-"*100)
    counter += 1

    hashtagList = ['워터파크', '비키니', '운동하는여자', '얼스타그램', '셀카', '셀피', '몸스타그램', '셀스타그램', '이태원', '홍대', '모노키니', '원피스', '여행스타그램', '리버풀',
                   '모델', '아시안게임', '갓의조', '빛빛빛', '롤', '배그', '아이유', '아이린', '조현', '베리굿', '직캠', '나연', '지효', '경리', '보미', '코스프레']
    hashtagRandom = random.choice(hashtagList)
    contentList = searchCrawling(hashtagRandom)

    infodict = {'contentname': names, 'like': like, 'image': image, 'content': content, 'list': contentList}
    return infodict
