#네이버 속보 뉴스
from bs4 import BeautifulSoup
import requests

#https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=100

def naver_news_it():

    #for sid in sids:
    url=f'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=105'
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

    return list(zip(titles_new,images_new,summary_new,companies_new))

if __name__ =='__main__':
    news = naver_news_it()
    print(news)

    # for article,img,summary,company in news:
    #     title, link = article
    #     print(f'제목:{title},주소:{link},이미지:{img}')
    #     print(f'요약:{summary},신문사:{company}')


