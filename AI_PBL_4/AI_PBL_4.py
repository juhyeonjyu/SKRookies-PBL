import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

"""
웹 서버 로그 기반 악성 요청 탐지를 위한 분류 모델 구축
로그 데이터 전처리 및 성능 지표(Accuracy, F1 등)를 활용한 모델 평가

웹 서버 로그 데이터를 분석하여 악성 요청을 탐지하는 머신러닝 분류 모델을 구축해야 합니다.
"""

# 데이터 불러오기
df = pd.read_csv('web_server_logs_2.csv')

# 데이터 확인
df.head()

# timestamp에서 hour 추출
df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
# df.head()

# is_error label 생성
# status_code가 400 이상인 경우 Error로 간주
df['is_error'] = df['status_code'].apply(lambda x: 1 if x >= 400 else 0)
# df.tail()

# size 열 표준화
scaler = StandardScaler()
df['size'] = scaler.fit_transform(df[['size']])

# method 열 원-핫 인코딩
df = pd.get_dummies(df, columns=['method'])

# 학습용과 테스트용 데이터 분할
X = df[['hour', 'size', 'method_GET', 'method_POST', 'method_PUT', 'method_DELETE']]
y = df['is_error']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Logistic Regression 모델 학습
# 클래스 불균형 문제를 해결하기 위해 class_weight='balanced' 사용
model = LogisticRegression(class_weight='balanced')
model.fit(X_train, y_train)

# 모델 평가
y_pred = model.predict(X_test)
print('[Classification Report]')
print('=' * 55)
print(classification_report(y_test, y_pred))

print('모델 평가 결과 분석 : ')
print('Recall : 악성 요청 탐지는 꽤 잘 되고 있으나 정상 요청을 놓치는 경우가 많습니다.')
print('F1-score : 악성 요청은 성능이 양호한 편이지만 정상 요청에 대한 성능 개선이 필요합니다.')