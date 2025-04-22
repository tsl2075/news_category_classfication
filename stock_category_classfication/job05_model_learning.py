import os
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Embedding, Conv1D, MaxPooling1D, LSTM, Dropout, Dense
from keras.models import load_model

x_train = np.load('./preprocessed/x_train.npy', allow_pickle=True)
x_test = np.load('./preprocessed/x_test.npy', allow_pickle=True)
y_train = np.load('./preprocessed/y_train.npy', allow_pickle=True)
y_test = np.load('./preprocessed/y_test.npy', allow_pickle=True)
print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)

# ✅ 단어 수 계산
word_size = np.max(x_train) + 1  # 또는 token 저장된 값 사용
max_len = x_train.shape[1]       # 입력 길이

# ✅ 모델 구성
model = Sequential([
    Embedding(word_size, 300, input_length=max_len), # 임베딩자동 계산으로 바꾸기
    Conv1D(64, kernel_size=5, padding='same', activation='relu'),
    MaxPooling1D(pool_size=2),
    LSTM(128, return_sequences=True),
    Dropout(0.3),
    LSTM(64),
    Dense(128, activation='relu'),
    Dense(y_train.shape[1], activation='softmax')  # 라벨 개수 자동 반영
])
model.summary()

# ✅ 컴파일 및 학습
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

fit_hist = model.fit(x_train, y_train, epochs=10, batch_size=128,
                     validation_data=(x_test, y_test))

# ✅ 평가 및 저장
score = model.evaluate(x_test, y_test, verbose=0)
print('🎯 최종 정확도:', score[1])

os.makedirs('./models', exist_ok=True)
model.save(f'./models/news_section_model_{score[1]:.4f}.h5')

# ✅ 시각화
plt.plot(fit_hist.history['accuracy'], label='Train Acc')
plt.plot(fit_hist.history['val_accuracy'], label='Val Acc')
plt.title('Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)
plt.show()




































