# 1. 패키지 호출하기
from flask import request
from flask_restful import Resource
from bs4 import BeautifulSoup  # BeautifulSoup 모듈을 호출
import requests


# 2. 클래스 정의하기
class bs4_newsCrawling(Resource):
    def get(self):
        news_type = request.args.get('searchtype')
        print(f'전달받은  값 : {news_type}')
        results = naver_news_it(news_type)
        print(f'실행 결과 - {results}')
        return results


# 3. 네이버 뉴스 크롤링 함수 정의하기
def naver_news_it(news_type):
    # Naver 뉴스 URL을 구성
    url = f'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1={news_type}'
    # 해당 URL로 GET 요청을 보내고 응답 받기
    res = requests.get(url)
    source = res.text  # 응답 텍스트를 가져옴
    soup = BeautifulSoup(source, 'html.parser')  # BeautifulSoup으로 HTML을 파싱

    # 뉴스 제목의 선택자를 입력하여 데이터 가져오기
    titles_1 = soup.select(
        '#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt:nth-child(2) > a')
    titles_2 = soup.select('#main_content > div.list_body.newsflash_body > ul.type06 > li > dl > dt:nth-child(2) > a')
    titles = titles_1 + titles_2

    titles_new = []  # 제목을 저장할 리스트
    for a in titles:
        titles_new.append((a.get_text().strip(), a['href']))

    # 뉴스 이미지의 선택자를 입력하여 이미지 정보 가져오기
    images_1 = soup.select(
        '#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt.photo > a > img')
    images_2 = soup.select('#main_content > div.list_body.newsflash_body > ul.type06 > li > dl > dt.photo > a > img')
    images = images_1 + images_2
    images_new = []  # 이미지를 저장할 리스트

    # 선택된 이미지 주소를 순회하며 추출
    for img in images:
        images_new.append(img.get('src'))

    # 신문사의 선택자를 입력하여 신문사 정보 가져오기
    companies_1 = soup.select(
        '#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dd > span.writing')
    companies_2 = soup.select('#main_content > div.list_body.newsflash_body > ul.type06 > li > dl > dd > span.writing')
    companies = companies_1 + companies_2
    companies_new = []  # 신문사를 저장할 리스트

    # 선택된 신무사 이름을 순회하며 추출
    for span in companies:
        companies_new.append(span.get_text())  # 신문사 이름 저장

    # 뉴스 요약의 선택자로 요약 정보 가져오기
    summary_1 = soup.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dd > span')
    summary_2 = soup.select('#main_content > div.list_body.newsflash_body > ul.type06 > li > dl > dd > span')
    summary = summary_1 + summary_2
    summary_new = []  # 요약을 저장할 리스트

    # 선택된 요약을 순회하며 추출
    for span in summary:
        summary_new.append(span.get_text())  # 요약 저장

    # 뉴스의 날짜 정보 가져오기
    date_1 = soup.select(
        '#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dd > span.date.is_new')
    date_2 = soup.select(
        '#main_content > div.list_body.newsflash_body > ul.type06 > li > dl > dd > span.date.is_new')
    date = date_1 + date_2
    date_new = []

    for span in date:
        date_new.append(span.get_text())


    # 최종적으로 제목, 링크, 이미지, 요약, 신문사 정보를 포함하는 딕셔너리 리스트를 반환
    return [
        {
            'title': title,
            'link': link,
            'imageUrl': image,
            'summary': summary,
            'company': company,
            'date':date
        }
        for (title, link), image, summary, company, date in zip(titles_new, images_new, summary_new, companies_new, date_new)
        # 각 리스트에서 데이터 추출
    ]


"""
 정치 : 100
 경제 : 101
 사회 : 102
 생활/문화 : 103
 IT/과학 : 105
"""
