from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ✅ 1. 크롬 옵션 설정
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# ✅ 2. top50 CSV에서 티커 목록 불러오기
df_top50 = pd.read_csv('./crawling_stock_data/stock_title_data/top25_stock_titles_total.csv')  # 파일명은 실제 이름으로 수정
tickers = df_top50['ticker'].dropna().unique().tolist()
print(f"🔍 총 {len(tickers)}개 티커 로드됨")

# ✅ 티커와 카테고리를 딕셔너리로 매핑
ticker_to_category = dict(zip(df_top50['ticker'], df_top50['category']))

# ✅ 3. 크롤링 결과 저장 리스트
news_data = []

# ✅ 4. 각 티커별 뉴스 페이지 크롤링
for ticker in tickers:
    print(f"📡 {ticker} 뉴스 수집 시작")
    url = f'https://finance.yahoo.com/quote/{ticker}/news'
    driver.get(url)
    time.sleep(3)  # 로딩 대기

    # 스크롤 내려서 뉴스 더 로딩
    for _ in range(35):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)

    # ✅ 뉴스 기사 카드들 가져오기 (h3 포함된 기사 링크 기준)
    try:
        articles = driver.find_elements(By.XPATH, '//ul/li//h3/ancestor::a')
        if len(articles) == 0:
            raise Exception("뉴스 없음")
    except:
        print(f"❌ {ticker} 뉴스 로딩 실패")
        continue

    print(f"📰 {ticker} 뉴스 {len(articles)}개 탐지됨")

    for article in articles[:200]:
        try:
            title = article.find_element(By.TAG_NAME, 'h3').text
            summary = article.find_element(By.TAG_NAME, 'p').text

            if len(summary) > 150:
                summary = summary[:150] + "..."

            news_data.append({
                'ticker': ticker,
                'title': title,
                'summary': summary,
                'category': ticker_to_category.get(ticker, 'Unknown')  # 매핑 안 되면 Unknown 처리
            })

        except Exception:
            continue

driver.quit()

# ✅ 5. 데이터프레임으로 변환 & 저장
df_news = pd.DataFrame(news_data)
df_news.to_csv('top25_ticker_news_total_200.csv', index=False, encoding='utf-8-sig')
print("✅ 전체 뉴스 CSV 저장 완료: top25_ticker_news_total_200.csv")