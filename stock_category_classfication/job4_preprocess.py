import pandas as pd
import numpy as np
import re
import nltk
import pickle
import os
from nltk.corpus import stopwords
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

# ✅ 불용어 다운로드
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# ✅ CSV 파일 로드
df = pd.read_csv('./top25_news_total.csv')
df.columns = df.columns.str.lower().str.strip()  # 컬럼 정리

# ✅ 전처리 대상: title + summary 결합
df['text'] = df['title'].astype(str) + ' ' + df['summary'].astype(str)

# ✅ 텍스트 정제 함수 정의
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z ]', ' ', text)
    words = text.split()
    words = [w for w in words if w not in stop_words and len(w) > 1]
    return ' '.join(words)

df['cleaned'] = df['text'].apply(clean_text)

# ✅ 입력(X), 정답(Y) 나누기
X = df['cleaned']
Y = df['category']

# ✅ 라벨 인코딩
encoder = LabelEncoder()
encoded_y = encoder.fit_transform(Y)
onehot_y = to_categorical(encoded_y)

# ✅ 토크나이저
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X)
seqs = tokenizer.texts_to_sequences(X)

max_len = max(len(s) for s in seqs)
x_pad = pad_sequences(seqs, maxlen=max_len)

# ✅ 데이터 분할
x_train, x_test, y_train, y_test = train_test_split(x_pad, onehot_y, test_size=0.2, random_state=42)

# ✅ 저장
os.makedirs('./preprocessed', exist_ok=True)
np.save('./preprocessed/x_train.npy', x_train)
np.save('./preprocessed/x_test.npy', x_test)
np.save('./preprocessed/y_train.npy', y_train)
np.save('./preprocessed/y_test.npy', y_test)

with open(f'./preprocessed/tokenizer_maxlen{max_len}.pickle', 'wb') as f:
    pickle.dump(tokenizer, f)

with open('models/label_encoder.pickle', 'wb') as f:
    pickle.dump(encoder, f)

# ✅ 완료 로그
print("🎉 전처리 완료!")
print(f"📦 시퀀스 최대 길이: {max_len}")
print(f"🏷️ 클래스 목록: {encoder.classes_.tolist()}")