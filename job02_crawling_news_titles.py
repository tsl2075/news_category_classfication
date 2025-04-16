from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time

options = ChromeOptions()

options.add_argument('lang=ko_KR')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

ur1 = 'https://news.naver.com/section/100'
driver.get(ur1)
time.sleep(5)
button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]'
for i in range(10):
    time.sleep(0.5)
    driver.find_element(By.XPATH, button_xpath).click()
time.sleep(5)

for i in range(1, 5):
    for j in range(1, 7):
        title_path = '//*[@id="newsct"]/div[4]/div/div[{}]/div[1]/ul/li[{}]/div/div/div[2]/a/strong'.format(i, j)
# 바뀌는 숫자에 i와 j 값을 for문 돌릴거임
    try:
        title = driver.find_element(By.XPATH, title_path).text
        print(title)
    except:
        print('error', i, j)



#제목을 xpath 해옴
'//*[@id="_SECTION_HEADLINE_LIST_dxkjh"]/li[1]/div/div/div[2]/a/strong'
'//*[@id="newsct"]/div[4]/div/div[1]/div[2]/ul/li[1]/div/div/div[2]/a/strong'
'//*[@id="newsct"]/div[4]/div/div[1]/div[2]/ul/li[2]/div/div/div[2]/a/strong'
'//*[@id="newsct"]/div[4]/div/div[1]/div[2]/ul/li[4]/div/div/div[2]/a/strong'
'//*[@id="newsct"]/div[4]/div/div[1]/div[4]/ul/li[1]/div/div/div[2]/a/strong'
'//*[@id="newsct"]/div[4]/div/div[1]/div[3]/div/a'
# 규칙을 찾으면 맨 앞에 [1]은 변함이 없고 뒤의 숫자만 바뀌기 때문에 이중for문으로 코드짬
# 도중에 error가 나는 건 맨 밑에 i와j를 제대로 넣을 수 없기 때문에 이런 주소는 제외처리를 해줘야 함







