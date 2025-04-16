from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
df_titles = pd.DataFrame()

for i in range(6):
    ur1 = 'https://news.naver.com/section/10{}'.format(i)  # 네이버의 정치페이지의 주소 복사 붙여넣기 함
    #ur2 = 'https://news.naver.com/section/101'

    resp = requests.get(ur1)
    soup = BeautifulSoup(resp.text, 'html.parser')

    # print(list(soup))
    title_tags = soup.select('.sa_text_strong')
    titles = []
    for tag in title_tags:
        titles.append(tag.text)
    print(titles)
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles],
                           axis='rows', ignore_index=True)
print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())
df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index=False)