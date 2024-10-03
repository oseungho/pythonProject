'''
pip install selenium
'''

import os # 운영 체제와 상호작용하는 기능을 제공하는 모듈
from selenium.webdriver.support import expected_conditions as EC

from selenium.common import NoSuchElementException, TimeoutException # Selenium의 예외 클래스
from selenium import webdriver # Selenium의 웹드라이버 클래스
from selenium.webdriver.chrome.service import Service # Chrome 웹드라이버 서비스를 위한 클래스
import time # 시간 관련 기능을 제공하는 모듈
from selenium.webdriver.common.by import By # 웹 요소를 찾기 위한 위치 전략 클래스
from flask import request  # Flask의 요청 객체를 가져오는 클래스
from flask_restful import Resource  # Flask-RESTful의 리소스 클래스
from selenium.webdriver.common.keys import Keys  # 키보드 입력을 시뮬레이션하는 클래스
from selenium.webdriver.support.wait import WebDriverWait


# Flask-RESTful의 Resource를 상속받아, API 엔드포인트를 정의하는 클래스
class youtubeCrawling(Resource):
    def get(self) : # HTTP GET 요청을 처리하는 메서드
        search = request.args.get('search') # 쿼리 파라미터에서 'search' 값을 가져옴
        searchtype = int(request.args.get('searchtype'))
        if search is None: # 'search' 파라미터가 없는 경우, 클라이언트에게 오류 메세지 반환
            return {'message' : '검색어를 전달해주세요.'}, 400 # 검색어가 전달되지 않았을 때의 예외 처리

        print('전달받은 값:', search, ' / ', searchtype) # 콘솔에 전달받은 search 출력
        result = youtube_crawling(search, searchtype) # 사용자 정의 함수 호출
        return {'result': result, 'searchtype': searchtype} # 작업이 완료된 후 반환

def youtube_crawling(search, searchtype):
    print('유튜브 크롤링을 시작합니다.') # 사용자 정의 함수가 정상적으로 실행됐는지 체크할 겸 작성

    try:
        # 1. WebDriver객체 생성
        # 현재 파일의 상위 디렉토리에서 'driver/chromedriver.exe'의 경로를 설정
        # chromedriver.exe가 다른 디렉토리 경로에 있으니 상위 디렉토리를 참조하여 'driver/chromedriver.exe'를 설정
        driver_path = f'{os.path.join(os.path.dirname(os.path.dirname(__file__)), "driver/chromedriver.exe")}'

        # 웹드라이버를 위한 Service 객체 생성
        service = Service(executable_path=driver_path)
        options = webdriver.ChromeOptions() # Chrome 브라우저의 옵션 설정 객체 생성
        options.add_argument("--headless")  # headless 모드 설정 -> 주석을 해제 시, 원격 제어 브라우저 창이 보이지 않음
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")  # 사용자 에이전트 설정

        # 에이전트 설정을 하는 이유?
        # 자동화된 스크립트나 봇을 차단하기 위해 브라위저의 기본 사용자 에이전트를 검사할 수 있어서 위 코드를 통해 차단 우회

        # 자동종료 막기
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(service=service, options=options) # Chrome 브라우저를 실행하는 WebDriver 객체 생성

        # 명시적 대기(Explicit Wait)
        wait = WebDriverWait(driver, 10)

        # 암시적 대기 설정: 최대 10초 동안 대기
        driver.implicitly_wait(10)

        # 2.브라우저에 네이버 페이지 로딩하기
        driver.get('https://www.youtube.com/')
        # time.sleep(3)  # 페이지가 완전히 로딩되도록 3초동안 기다림

        # 검색 박스 요소를 찾기 위한 XPATH
        search_box = driver.find_element(By.XPATH,'//*[@id="search-input"]/input')

        # 검색어 입력 및 검색 버튼 클릭 시뮬레이션
        search_box.send_keys(search)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

        print(f'type에 따른 실행함수 분기 - {searchtype}, class : {type(searchtype)}')
        if(searchtype == 1):
            print('광고 정보를 크롤링합니다.')
            # info_list = driver.find_elements(By.XPATH, '//*[@id="sparkles-body"]')

            # presence_of_all_elements_located는 여러 요소가 DOM에 로드되어있는지 확인
            info_list = wait.until(EC.presence_of_all_elements_located(By.XPATH, '//*[@id="sparkles-body"]'))
            info_result = advertisement_crawling(info_list)
        elif (searchtype == 2):
            print('쇼츠 정보를 크롤링합니다.')
            info_list = driver.find_elements(By.XPATH, '//*[@id="items"]/ytm-shorts-lockup-view-model-v2[*]')
            info_result = short_crawling(info_list)
        else:
            print('영상 정보를 크롤링합니다.')
            info_list = driver.find_elements(By.XPATH, '//*[@id="sparkles-body"]')
            #'//*[@id="video-title"]'#
            info_result = video_crawling(info_list)

        print('info_result : ', info_result)

        return info_result


    except (TimeoutException, NoSuchElementException) as e: # 웹 요소를 찾을 수 없거나 타임아웃이 발생한 경우 예외 처리
        print('지정한 요소를 찾을수 없어요:', e)

    finally:
        pass
        #driver.quit() # WebDriver 종료
def advertisement_crawling(info_list):
    advertisement_dic = {}
    print('수집 값 :', info_list)

    index = 1
    for ad in info_list:
        ad_title = ad.find_element(By.XPATH, './h3').text
        ad_description = ad.find_elements(By.XPATH, './div')[0].text
        print(f'INDEX : {index}, 제목 : {ad_title}, 설명 : {ad_description}')

        data = {
            'index' : index,
            'title' : ad_title,
            'description' : ad_description
        }

        advertisement_dic[index] = data
        index += 1
    return advertisement_dic


def short_crawling(info_list):
    short_dic = {}
    idx = 1
    for info in info_list:
        print(f'info - {type(info)}')
        href = info.find_element(By.XPATH, './ytm-shorts-lockup-view-model/a').get_attribute('href')
        image = info.find_element(By.XPATH, './ytm-shorts-lockup-view-model/a/div/img').get_attribute('src')
        title = info.find_element(By.XPATH, './ytm-shorts-lockup-view-model/div/h3/a/span').text
        print(f'index:{idx}, title-{title}, href-{href}, image-{image}')

        data = {
            'index': idx,
            'title': title,
            'href' : href,
            'image': image
        }
        short_dic[idx] = data
        idx += 1
    return short_dic

def video_crawling(info_list):
    video_dic = {}
    idx = 1
    return 0