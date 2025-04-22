# import pandas as pd
# import glob
#
# data_dir = './crawling_stock_data/stock_title_data/'
# data_path = glob.glob(data_dir + '*.*')
# print(data_path) #경로에 해당하는 파일이 있는지
#
# df = pd.DataFrame()
# for path in data_path:
#     df_section = pd.read_csv(path)
#     df = pd.concat([df, df_section], ignore_index=True)
# df.info()
# print(df.head())
# df.to_csv('./crawling_stock_data/top25_stock_titles_total.csv', index=False)


#파일합치기
import pandas as pd
import glob

# ✅ 1. CSV 파일 경로들 가져오기
file_list = glob.glob('./news_by_sector/*.csv')  # 폴더 경로에 맞게 수정

# ✅ 2. 파일들을 하나씩 읽어서 리스트에 담기
df_list = [pd.read_csv(file) for file in file_list]

# ✅ 3. 하나의 데이터프레임으로 합치기
merged_df = pd.concat(df_list, ignore_index=True)

# ✅ 4. 중복 제거 (필요 시)
merged_df.drop_duplicates(inplace=True)

# ✅ 5. 저장
merged_df.to_csv('./merged_sector_news_total.csv', index=False, encoding='utf-8-sig')
print("✅ 합친 CSV 저장 완료: merged_sector_news_total.csv")

