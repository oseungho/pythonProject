import os
import time

from flask import request
from flask_restful import Resource
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class newsCrawling(Resource):
    def get(self):
        news_type = request.args.get('searchtype')
        print(f'전달받은  값 : {news_type}')
        results = naver_news(news_type)
        print(f'실행 결과 - {results}')
        return 0

def naver_news(news_type):
    print('뉴스 크롤링을 시작합니다.')

    driver_path = f'{os.path.join(os.path.dirname(os.path.dirname(__file__)), "driver/chromedriver.exe")}'
    service = Service(executable_path=driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") #-- 사용자에게 정보를 크롤링하는 화면을 보여주지 않기 위해서 (주석 풀었을 때)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")

    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f'https://news.naver.com/section/{news_type}')
    time.sleep(3)

    news_infos = driver.find_elements(By.XPATH, '/html/body/div/div[2]/div[2]/div[2]/div[1]/div[1]/ul/li[*]')
    idx = 1

    for news_info in news_infos:
        news_title = news_info.find_element(By.XPATH, './div/div/div[2]/a/strong').text
        news_href = news_info.find_element(By.XPATH, './div/div/div[2]/a').get_attribute('href')

        print(f"""[{idx}번째 기사 정보] 
                  기사 제목 : {news_title}, 
                  기사 링크 : {news_href}""")

        idx += 1
    # /div/div/div[2]/a/strong'

    return '성공'

# https://news.naver.com/section/
"""
 정치 : 100
 경제 : 101
 사회 : 102
 생활/문화 : 103
 IT/과학 : 105
"""