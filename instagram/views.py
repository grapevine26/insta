from django.shortcuts import render
from search import searchCrawling
from detail import detailCrawling
import random
def home(request):
    hashtagList = ['워터파크', '비키니', '운동하는여자', '얼스타그램', '셀카', '셀피', '몸스타그램', '셀스타그램', '이태원', '홍대', '모노키니', '원피스', '여행스타그램', '리버풀',
                   '모델', '아시안게임', '갓의조', '빛빛빛', '롤', '배그', '아이유', '아이린', '조현', '베리굿', '직캠', '나연', '지효', '경리', '보미', '코스프레']
    hashtagRandom = random.choice(hashtagList)
    contentList = searchCrawling(hashtagRandom)
    return render(request, 'home.html', {'contentList': contentList})

def detail(request, hrefs):
    userURL = hrefs
    lists = detailCrawling(userURL)
    return render(request, 'detail.html', {'list': lists})

def list(reqeust, *args, **kwargs):
    hashtag = reqeust.POST.get('search')
    contentDICT = searchCrawling(hashtag)
    return render(reqeust, 'list.html', {'content': contentDICT})
