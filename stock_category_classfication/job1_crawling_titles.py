from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import datetime

options = ChromeOptions()

service = ChromeService(executable_path=ChromeDriverManager().install()) # 크롬 드라이버 설치
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

category = ['Basic Materials', 'Communication Services', 'Consumer Cyclical', 'Consumer Defensive']
df_titles = pd.DataFrame()

print(category)

# 크롤링 대상 URL
url =  'https://finance.yahoo.com/research-hub/screener/sec-ind_ind-largest-equities_software-infrastructure/?start=0&count=100'
driver.get(url)
time.sleep(5)

button_sector_delete1 = '//*[@id="nimbus-app"]/section/section/section/article/section/div/div[3]/div/div[5]/button/div'
button_sector_delete2 = '//*[@id="nimbus-app"]/section/section/section/article/section/div/div[3]/div/div[4]/button/div'
button_sector_select = '//*[@id="nimbus-app"]/section/section/section/article/section/div/div[3]/div/div[3]/div/button'
button_sector_tech = '//*[@id="Technology"]'
button_sector_Materials = '//*[@id="Basic Materials"]'
apply_xpath = '//button[text()="Apply" and not(@disabled)]'
button_select = '//*[@id="nimbus-app"]/section/section/section/article/section/div/div[5]/div[2]/div[1]/div/div/div/button'
button_select_100 = '//*[@id="opt-8234"]'
button_next = '//*[@id="nimbus-app"]/section/section/section/article/section/div/div[5]/div[2]/div[3]/button[3]'

# Energy 카테고리 필터 설정
try :
    driver.find_element(By.XPATH, button_sector_delete1).click()    # 필터 5 제거
    driver.find_element(By.XPATH, button_sector_delete2).click()    # 필터 4 제거
    driver.find_element(By.XPATH, button_sector_select).click()     # 섹터 선택창 클릭
    driver.find_element(By.XPATH, button_sector_tech).click()       # tech 해제
    driver.find_element(By.XPATH, button_sector_Materials).click()     # 섹터 클릭

    apply_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, apply_xpath)))

    apply_button.click()     # apply 섹터 클릭
    time.sleep(1)

except Exception as e:
    print("필터 설정 중 오류 발생")

# 결과 수집 시작
titles = []
tickers = []

print("page 1 수집중...")

for j in range(1, 101):
    try:
        ticker_xpath = f'//*[@id="nimbus-app"]/section/section/section/article/section/div/div[5]/div[1]/table/tbody/tr[{j}]/td[2]/div/span/a/div/span'
        name_xpath = f'//*[@id="nimbus-app"]/section/section/section/article/section/div/div[5]/div[1]/table/tbody/tr[{j}]/td[3]/div'

        ticker = wait.until(EC.presence_of_element_located((By.XPATH, ticker_xpath))).text
        name = wait.until(EC.presence_of_element_located((By.XPATH, name_xpath))).text

        tickers.append(ticker)
        titles.append(name)
        fail_count = 0
    except:
        print(f"기업 {j} 정보 수집 실패")
        fail_count += 1
        if fail_count >= 3:
            print("기업정보 3번 이상 실패, 수집 종료")
            break

    # # 다음 페이지 버튼 클릭
    # try :
    #     # 다음 페이지 버튼
    #     next_btn_x_path = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_next))).click()
    #     time.sleep(2)
    # except :
    #     print("다음 페이지 없음 또는 클릭 실패")
    #     break


df = pd.DataFrame({
    'ticker': tickers,
    'titles': titles
})

# ✅ 중복 제거 (순서 유지됨)
df = df.drop_duplicates(subset='titles', keep='first')

# ✅ 앞에서 50개만 선택
df = df.head(50)

# ✅ 카테고리 추가
df['category'] = 'Basic Materials'

# ✅ 저장
df.to_csv('20250421_top25_Basic_Materials.csv', index=False, encoding='utf-8-sig')
print("✅ 저장 완료!")

