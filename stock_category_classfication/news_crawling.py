from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import os
from datetime import datetime

# 메인 크롤링 함수 정의
def crawl_sector_news(sector, scroll_count=20): #scroll_count는 스크롤 횟수 조절 (뉴스를 더 많이 긁을 수 있음)
    print(f'📡 크롤링 시작: {sector}') # sector는 처리할 섹터명 (예: "technology")
    url = f'https://finance.yahoo.com/sectors/{sector}/'  #각 섹터의 뉴스 페이지에 접속

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(), options=options)
    driver.get(url)
    time.sleep(3)
#자동 스크롤 (동적 콘텐츠 로딩)
    for _ in range(scroll_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)

    titles = []
    summaries = []
    #뉴스 요소 추출
    ads = driver.find_elements(By.XPATH, '//div[contains(@id,"internal_trc_")]')
    articles = driver.find_elements(By.XPATH, '//ul/li/section/div/a')
    #광고는 id="internal_trc_..."로 식별 → 필터링 가능
    #뉴스는 <a> 태그 안에 h3(제목)과 p(요약)가 있음

    #필터링 & 텍스트 추출
    for article in articles:
        try:
            if article in ads:
                continue

            title_element = article.find_element(By.TAG_NAME, 'h3')
            summary_element = article.find_element(By.TAG_NAME, 'p')

            title = title_element.text.strip()
            summary = summary_element.text.strip()

            if len(summary) > 150:
                summary = summary[:150] + "..."

            if title and summary:
                titles.append(title)
                summaries.append(summary)
        except:
            continue

    driver.quit()

    #데이터프레임 + 저장
    df = pd.DataFrame({
        'title': titles,
        'summary': summaries,
        'category': [sector] * len(titles)
    })
    # 오늘 날짜 (예: '20250421')
    today = datetime.today().strftime('%Y%m%d')

    # 폴더 생성
    os.makedirs('news_by_sector', exist_ok=True)

    # 파일 저장 (예: news_consumer-defensive_20250421.csv)
    df.to_csv(f'news_by_sector/news_{sector}_{today}.csv', index=False, encoding='utf-8-sig')

    print(f'✅ 저장 완료: news_by_sector/news_{sector}.csv')

# 🔽 처리할 섹터 리스트
sector_list = [
    'basic-materials',
    'communication-services',
    'consumer-cyclical',
    'consumer-defensive'
]

for sector in sector_list:
    crawl_sector_news(sector, scroll_count=25)
