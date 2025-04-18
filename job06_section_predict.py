import pickle
import pandas as pd
import numpy as np
from keras.utils import to_categorical
from konlpy.tag import Okt
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import re

df = pd.read_csv('./crawling_data/naver_headline_news_20250418.csv')
df.drop_duplicates(inplace=True) #중복제거
df.reset_index(drop=True, inplace=True)
print(df.head())
df.info()
#print(df.category.value_counts())

# 전처리
X = df.titles
Y = df.category

with open('./models/encoder.pickle', 'rb') as f:# 전처리했던거랑 똑같이 해줘여함
    encoder = pickle.load(f)
label = encoder.classes_
#print(label) #라벨 그대로 가져와야 함

labeled_y = encoder.transform(Y) #이미정보를 가지고 있어서 라벨링만 할 땐 transform
onehot_y = to_categorical(labeled_y)
#print(onehot_y)

okt = Okt()
for i in range(len(X)):
    X[i] = re.sub('[^가-힣]', ' ', X[i])
    X[i] = okt.morphs(X[i], stem=True)
#print(X)

for idx, sentence in enumerate(X):
    words = []
    for word in sentence:
        if len(word) > 1:
            words.append(word)
    X[idx] = ' '.join(words)
print(X[:10])

with open('./models/token_max_25.pickle', 'rb') as f:
    token = pickle.load(f)

tokened_x = token.texts_to_sequences(X)
print(tokened_x[:5])

#25개 보다 길면 뒤쪽으로 짤라낸다
for i in range(len(tokened_x)):
    if len(tokened_x[i]) > 25:
        tokened_x[i] = tokened_x[i][:25]
x_pad = pad_sequences(tokened_x, 25)
print(x_pad)

model = load_model('./models/news_section_classfication_model_0.7293309569358826.h5')
preds = model.predict(x_pad)
print(preds)



predict_section = []
for pred in preds :
    most = label[np.argmax(pred)]
    pred[np.argmax([pred])] = 0
    second = label[np.argmax(pred)]
    predict_section.append([most, second])
    # predict_section.append(label[np.argmax(pred)])
print(predict_section)

df['predict'] = predict_section
print(df.head())

score = model.evaluate(x_pad, onehot_y)
print(score[1])

df['ox'] = 0
for i in range(len(df)):
    if df.loc[i, 'category'] in df.loc[i, 'predict']:
        df.loc[i, 'ox'] = 1

print(df.ox.mean())










