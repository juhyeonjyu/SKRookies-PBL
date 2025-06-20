import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

"""
주택 가격 데이터를 활요한 회귀 모델 학습 및 예측
DecisionTreeRegressor를 활용한 모델 구축 및 성능 평가

주택 가격 데이터를 기반으로 회귀 모델을 학습하여 주택 가격을 예측해야 합니다.
"""

# 데이터 불러오기
df = pd.read_csv('20250620_143716_train.csv')

# 데이터 정보 확인
df.info()

# 데이터 구조 확인
df.head()

# 결측값 처리
# 결측치 개수 확인
bf_counts = df.isnull().sum()
print(bf_counts[bf_counts > 0])

# 결측치가 500개 이상인 열 삭제
for col in df :
    if bf_counts[col] > 500 :
        df = df.drop(col, axis=1)

# 500개 이상 결측치 제거 확인
af_counts = df.isnull().sum()
print(af_counts[af_counts > 0])

# LotFrontage 열 평균으로 대체
df['LotFrontage'] = df['LotFrontage'].fillna(df['LotFrontage'].mean())

# 결과 확인
print(df['LotFrontage'].isnull().sum())

# 범주형 데이터 인코딩
categorical_cols = df.select_dtypes(include='object').columns
df = pd.get_dummies(df, columns=categorical_cols)

# 결과 확인
df.select_dtypes(include='object').columns

# 불필요한 Id 열 제거
df = df.drop(columns=['Id'], axis=1)

# 결과 확인
'Id' in df.columns

# 학습 및 테스트 데이터 분리 : 8:2 비율
X = df.drop('SalePrice', axis=1)    # Feature : 나머지 열
y = df['SalePrice']                 # Target : SalePrice

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 모델 학습
model = DecisionTreeRegressor()
model.fit(X_train, y_train)

# 모델 평가
pred = model.predict(X_test)

mae = mean_absolute_error(y_test, pred)
mse = mean_squared_error(y_test, pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, pred)

print('MAE(Mean Absolute Error; 평균 절대 오차): ', mae, ' > 작을수록 좋음')
print('MSE(Mean Squared Error; 평균 제곱 오차) : ', mse, ' > 작을수록 좋음')
print('RMSE(Root Mean Squared Error; 평균 제곱근 오차) : ', rmse, ' > 작을수록 좋음')
print('R^2(R-squared; 결정 계수) : ', r2, ' > 1에 가까울 수록 좋음')