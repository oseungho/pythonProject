# 1. 패키지 호출하기
import os # 운영 체제와 상호작용하는 기능을 제공하는 모듈
from selenium.webdriver.chrome.service import Service # Chrome 웹드라이버 서비스를 위한 클래스
from flask import request
from flask_restful import Resource
from bs4 import BeautifulSoup # BeautifulSoup 모듈을 호출
from selenium.common import NoSuchElementException, TimeoutException # Selenium의 예외 클래스
from selenium import webdriver # Selenium의 웹드라이버 클래스
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# 2. 클래스 정의하기
class newsCrawling(Resource):
    def get(self):
        news_type = request.args.get('searchtype')
        news_pages = request.args.get('searchText')

        print(f'전달받은  값 : {news_type}, {news_pages}')
        results = naver_news_it(news_type, news_pages)
        print(f'실행 결과 - {results}')
        return results

# 3. 크롤링 함수 정의하기
def naver_news_it(news_type, news_pages):

    try:
        # 1. WebDriver객체 생성
        driver_path = f'{os.path.join(os.path.dirname(os.path.dirname(__file__)), "driver/chromedriver.exe")}'

        # 웹드라이버를 위한 Service 객체 생성
        service = Service(executable_path=driver_path)
        options = webdriver.ChromeOptions()  # Chrome 브라우저의 옵션 설정 객체 생성
        options.add_argument("--headless")  # headless 모드 설정 -> 주석을 해제 시, 원격 제어 브라우저 창이 보이지 않음
        # 사용자 에이전트 설정
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(service=service, options=options)  # Chrome 브라우저를 실행하는 WebDriver 객체 생성

        # Naver 뉴스 URL을 구성
        driver.get(f'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1={news_type}')

        # 최종적으로 제목, 링크, 이미지, 요약, 신문사 정보를 포함하는 딕셔너리 리스트를 반환
        return repeat_crawling(driver, int(news_pages))

    except (TimeoutException, NoSuchElementException) as e: # 웹 요소를 찾을 수 없거나 타임아웃이 발생한 경우 예외 처리
        print('지정한 요소를 찾을수 없어요:', e)
        return []
    finally:
        # 모든 창을 종료하고 세션 종료
        driver.quit()

# 4. 동적으로 페이지를 넘어가며 크롤링하는 함수 정의하기
def repeat_crawling(driver, page_count):
    titles_new = []
    images_new = []
    summary_new = []
    companies_new = []
    date_new = []

    for page in range(1, page_count+1):
        print(f'현재 페이지 - {page}')
        # 해당 URL로 GET 요청을 보내고 응답 받기
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')  # BeautifulSoup으로 HTML을 파싱

        # 뉴스 제목의 선택자를 입력하여 데이터 가져오기
        titles_1 = soup.select(
            '#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt:nth-child(2) > a')
        titles_2 = soup.select('#main_content > div.list_body.newsflash_body > ul.type06 > li > dl > dt:nth-child(2) > a')
        titles = titles_1 + titles_2
        titles_new += [(a.get_text().strip(), a['href']) for a in titles]

        # 뉴스 이미지의 선택자를 입력하여 이미지 정보 가져오기
        images_1 = soup.select(
            '#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt.photo > a > img')
        images_2 = soup.select('#main_content > div.list_body.newsflash_body > ul.type06 > li > dl > dt.photo > a > img')
        images = images_1 + images_2
        # 선택된 이미지 주소를 순회하며 추출
        images_new += [img.get('src') for img in images]

        # 신문사의 선택자를 입력하여 신문사 정보 가져오기
        companies_1 = soup.select(
            '#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dd > span.writing')
        companies_2 = soup.select('#main_content > div.list_body.newsflash_body > ul.type06 > li > dl > dd > span.writing')
        companies = companies_1 + companies_2
        # 선택된 신무사 이름을 순회하며 추출
        companies_new += [span.get_text() for span in companies]

        # 뉴스 요약의 선택자로 요약 정보 가져오기
        summary_1 = soup.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dd > span.lede')
        summary_2 = soup.select('#main_content > div.list_body.newsflash_body > ul.type06 > li > dl > dd > span.lede')
        summary = summary_1 + summary_2

        # 선택된 요약을 순회하며 추출
        summary_new += [span.get_text() for span in summary]

        # 뉴스의 날짜 정보 가져오기
        date_1 = soup.select(
            '#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dd > span.date.is_new')
        date_2 = soup.select(
            '#main_content > div.list_body.newsflash_body > ul.type06 > li > dl > dd > span.date.is_new')
        date = date_1 + date_2
        date_new += [span.get_text() for span in date]

        # 각 리스트에 데이터가 얼마나 들어있는지 출력
        print(f"""페이지 {page}에서 수집된 데이터 개수:
                  제목: {len(titles_new)}개, 이미지: {len(images_new)}개, 신문사: {len(companies_new)}개, 
                  요약: {len(summary_new)}개, 날짜: {len(date_new)}개""")

        next_btn = soup.select(f'#main_content > div.paging > a:nth-child({page+1})')
        if next_btn:
            try:
                # Selenium으로 '다음 페이지 버튼을 클릭'
                next_button_element = driver.find_element(By.CSS_SELECTOR,
                                                          f'#main_content > div.paging > a:nth-child({page+1})')
                next_button_element.click()

                # JavaScript로 페이지의 로딩 상태를 확인하는 방법
                WebDriverWait(driver, 10).until(
                    lambda driver: driver.execute_script('return document.readyState') == 'complete'
                )

            except TimeoutException as e:
                print(f'페이지 {page}에서 타임아웃 오류 발생 : ', e)
                break
            except NoSuchElementException as e:
                print(f'페이지 {page}에서 요소를 찾지 못하는 오류 발생 :  ', e)
                break
        else:
            break

    # 크롤링한 데이터 반환
    return [
        {
            'title': title,
            'link': link,
            'imageUrl': image,
            'summary': summary,
            'company': company,
            'date': date
        }
        for (title, link), image, summary, company, date in
        zip(titles_new, images_new, summary_new, companies_new, date_new)
    ]
