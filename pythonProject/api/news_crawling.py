from flask import request
from flask_restful import Resource
from bs4 import BeautifulSoup
import requests


class newsCrawling(Resource):
    def get(self):
        news_type = request.args.get('searchtype')
        print(f'전달받은  값 : {news_type}')
        results = naver_news_it(news_type)
        print(f'실행 결과 - {results}')
        return results

def naver_news_it(news_type):

    # Naver 뉴스 URL을 구성
    url=f'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1={news_type}'
    res = requests.get(url)
    source = res.text
    soup = BeautifulSoup(source,'html.parser')
    #제목
    titles=soup.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt:nth-child(2) > a')
    titles_new=[]
    for a in titles:
        titles_new.append((a.get_text().strip(),a['href']))
    #이미지 주소
    images = soup.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt.photo > a > img')
    images_new = []
    for img in images:
        images_new.append(img.get('src'))
    #신문사
    companies = soup.select(
        '#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dd > span.writing')
    companies_new = []
    for span in companies:
        companies_new.append(span.get_text())
    #요약
    summary=soup.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dd > span')
    summary_new = []
    for span in summary:
        summary_new.append(span.get_text())

    return [
        {
            'title': title,
            'link': link,
            'imageUrl': image,
            'summary': summary,
            'company': company
        }
        for (title, link), image, summary, company in zip(titles_new, images_new, summary_new, companies_new)
    ]


"""
 정치 : 100
 경제 : 101
 사회 : 102
 생활/문화 : 103
 IT/과학 : 105
"""