import pandas as pd
import glob

data_dir = './news_by_sector/'
data_path = glob.glob(data_dir + '*.*')
print(data_path) #경로에 해당하는 파일이 있는지

df = pd.DataFrame()
for path in data_path:
    df_section = pd.read_csv(path)
    df = pd.concat([df, df_section], ignore_index=True)
df.info()
print(df.head())
df.to_csv('./news_by_sector/stock_titles_total.csv', index=False)
