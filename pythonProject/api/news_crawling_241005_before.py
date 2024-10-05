import os # 운영 체제와 상호작용하는 기능을 제공하는 모듈
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service # Chrome 웹드라이버 서비스를 위한 클래스
from flask import request
from flask_restful import Resource
from bs4 import BeautifulSoup # BeautifulSoup 모듈을 호출
from selenium.common import NoSuchElementException, TimeoutException # Selenium의 예외 클래스
from selenium import webdriver # Selenium의 웹드라이버 클래스
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class newsCrawling(Resource):
    def get(self):
        news_type = request.args.get('searchtype')
        print(f'전달받은  값 : {news_type}')
        results = naver_news_it(news_type)
        print(f'실행 결과 - {results}')
        return results

def naver_news_it(news_type):

    try:
        # 1. WebDriver객체 생성
        driver_path = f'{os.path.join(os.path.dirname(os.path.dirname(__file__)), "driver/chromedriver.exe")}'

        # 웹드라이버를 위한 Service 객체 생성
        service = Service(executable_path=driver_path)
        options = webdriver.ChromeOptions()  # Chrome 브라우저의 옵션 설정 객체 생성
        #options.add_argument("--headless")  # headless 모드 설정 -> 주석을 해제 시, 원격 제어 브라우저 창이 보이지 않음
        #options.add_argument('--disable-popup-blocking')  # 팝업 차단 비활성화
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")  # 사용자 에이전트 설정
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(service=service, options=options)  # Chrome 브라우저를 실행하는 WebDriver 객체 생성

        # Naver 뉴스 URL을 구성
        driver.get(f'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1={news_type}')

        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "")))

        # 해당 URL로 GET 요청을 보내고 응답 받기
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser') # BeautifulSoup으로 HTML을 파싱

        # 뉴스 제목의 선택자를 입력하여 데이터 가져오기
        titles_1=soup.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt:nth-child(2) > a')
        titles_2=soup.select('#main_content > div.list_body.newsflash_body > ul.type06 > li > dl > dt:nth-child(2) > a')

        titles = titles_1 + titles_2

        titles_new=[] # 제목을 저장할 리스트
        for a in titles:
            titles_new.append((a.get_text().strip(),a['href']))

        # 뉴스 이미지의 선택자를 입력하여 이미지 정보 가져오기
        images_1 = soup.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt.photo > a > img')
        images_2 = soup.select('#main_content > div.list_body.newsflash_body > ul.type06 > li > dl > dt.photo > a > img')
        images = images_1 + images_2
        images_new = [] # 이미지를 저장할 리스트

        # 선택된 이미지 주소를 순회하며 추출
        for img in images:
            images_new.append(img.get('src'))

        # 신문사의 선택자를 입력하여 신문사 정보 가져오기
        companies_1 = soup.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dd > span.writing')
        companies_2 = soup.select('#main_content > div.list_body.newsflash_body > ul.type06 > li > dl > dd > span.writing')
        companies = companies_1 + companies_2
        companies_new = [] # 신문사를 저장할 리스트

        # 선택된 신무사 이름을 순회하며 추출
        for span in companies:
            companies_new.append(span.get_text()) # 신문사 이름 저장

        # 뉴스 요약의 선택자로 요약 정보 가져오기
        summary_1=soup.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dd > span')
        summary_2 = soup.select('#main_content > div.list_body.newsflash_body > ul.type06 > li > dl > dd > span')
        summary = summary_1 + summary_2
        summary_new = [] # 요약을 저장할 리스트

        # 선택된 요약을 순회하며 추출
        for span in summary:
            summary_new.append(span.get_text()) # 요약 저장

        next_btn = soup.select('#main_content > div.paging > a:nth-child(2)')
        # 현재 페이지는 '#main_content > div.paging > strong' 으로 나옴 (시작은 a:nth-child(2) ~ 끝은 a:nth-child(11))

        if next_btn:
            # Selenium으로 '다음 페이지 버튼을 클릭'
            next_button_element = driver.find_element(By.CSS_SELECTOR, '#main_content > div.paging > a:nth-child(2)')
            next_button_element.click()

            # 클릭 후 새로운 페이지가 로드되도록 대기
            WebDriverWait(driver, 10).until(EC.staleness_of(next_button_element))  # 버튼이 더 이상 유효하지 않게 될 때까지 대기

            # 페이지 로드 후 다시 HTML 파싱
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            print(f'새로운 페이지 - {soup}')


        print(next_btn)

        # 최종적으로 제목, 링크, 이미지, 요약, 신문사 정보를 포함하는 딕셔너리 리스트를 반환
        return [
            {
                'title': title,
                'link': link,
                'imageUrl': image,
                'summary': summary,
                'company': company
            }
            for (title, link), image, summary, company in zip(titles_new, images_new, summary_new, companies_new) # 각 리스트에서 데이터 추출
        ]
    except (TimeoutException, NoSuchElementException) as e: # 웹 요소를 찾을 수 없거나 타임아웃이 발생한 경우 예외 처리
        print('지정한 요소를 찾을수 없어요:', e)

    finally:
        pass
