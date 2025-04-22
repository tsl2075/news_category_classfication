import pandas as pd
import numpy as np
import pickle
import re
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
import nltk
from nltk.corpus import stopwords

# ✅ 1. 데이터 로드
df = pd.read_csv('./merged_sector_news_total.csv')
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)

# ✅ 2. 텍스트 결합: title + summary
df['text'] = df['title'].astype(str) + ' ' + df['summary'].astype(str)

# ✅ 3. 라벨 정규화 (소문자-하이픈 → 타이틀케이스-공백)
def normalize_category(label):
    return label.replace('-', ' ').title().strip()

df['category'] = df['category'].apply(normalize_category)

# ✅ 4. 정답 라벨 인코더 로드
with open('./models/label_encoder.pickle', 'rb') as f:
    encoder = pickle.load(f)

label = encoder.classes_
valid_labels = set(label)

# ✅ 5. 유효한 카테고리만 필터링
df = df[df['category'].isin(valid_labels)].reset_index(drop=True)

# ✅ 6. 라벨 인코딩
labeled_y = encoder.transform(df['category'])
onehot_y = to_categorical(labeled_y)

# ✅ 7. 텍스트 전처리 (영어용)
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z ]', ' ', text)
    words = text.split()
    words = [w for w in words if w not in stop_words and len(w) > 1]
    return ' '.join(words)

df['cleaned'] = df['text'].apply(clean_text)

# ✅ 8. 토크나이저 로드 + 시퀀스 + 패딩
with open('./models/tokenizer_maxlen25.pickle', 'rb') as f:
    tokenizer = pickle.load(f)

tokened = tokenizer.texts_to_sequences(df['cleaned'])
x_pad = pad_sequences(tokened, maxlen=25)
print(x_pad)

# ✅ 9. 모델 로드
model = load_model('./models/news_section_model_0.8567.h5')  # 모델 파일명에 맞게 수정하세요

# ✅ 10. 예측 수행
preds = model.predict(x_pad)
print(preds)

# ✅ 11. 상위 2개 예측 추출
predict_section = []
for pred in preds:
    most_idx = np.argmax(pred)
    most = label[most_idx]
    pred[most_idx] = 0
    second = label[np.argmax(pred)]
    predict_section.append([most, second])
print(predict_section)

df['predict'] = predict_section
print(df.head())

# ✅ 12. 정확도 평가
df['ox'] = df.apply(lambda row: int(row['category'] in row['predict']), axis=1)
accuracy = df['ox'].mean()
print(f"✅ 예측 정확도: {accuracy * 100:.2f}%")

# ✅ 13. 결과 저장
df.to_csv('./predicted_sector_news.csv', index=False, encoding='utf-8-sig')
print("📄 예측 결과 저장 완료: predicted_sector_news.csv")
