import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# 데이터 불러오기
df = pd.read_csv('customer_data_balanced.csv')

# 데이터 확인
# df.head()

# ContractType 원-핫 인코딩
df = pd.get_dummies(df, columns=['ContractType'])

# Feature, Target 정의
X = df.drop('IsChurn', axis=1)
y = df['IsChurn']

# 정규화
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 학습 및 테스트 데이터 설정
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 모델 정의
model = models.Sequential([
    layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    layers.Dropout(0.3),
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(1, activation='sigmoid') # 이진 분류
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# 클래스 가중치
class_weights = {0: 1.0, 1: 2.0}

# EarlyStopping 콜백 정의
early_stop = callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# 모델 학습
history = model.fit(X_train, y_train,
                    epochs=50,
                    batch_size=32,
                    validation_split=0.2,
                    class_weight=class_weights,
                    callbacks=[early_stop],
                    verbose=1)

# 예측
y_pred_prob = model.predict(X_test)
y_pred = (y_pred_prob > 0.5).astype(int)

# 평가 지표 출력
print('Confusion Matrix : \n', confusion_matrix(y_test, y_pred))
print('\nClassification Report : \n', classification_report(y_test, y_pred))