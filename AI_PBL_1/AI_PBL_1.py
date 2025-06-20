import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

"""
당뇨병 진단 데이터를 활요한 데이터 전처리 및 EDA 분석
결측치 및 이상치 처리 방법 학습

당뇨병 진단 데이터를 기반으로 기초적인 데이터 전처리 및 탐색적 데이터 분석(EDA)을 수행하는 과제가 주어졌습니다.
"""

# 데이터 불러오기
df = pd.read_csv('20250618_175248_diabetes.csv')

# 데이터 정보 확인
df.info()

# 데이터 구조 확인
df.head()

# 데이터 통계 요약 정보 확인
df.describe()

# 결측치 처리
# 0을 결측치로 간주
with_zeros = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
for col in with_zeros :
    df[col] = df[col].replace(0, np.nan)
# 결측치를 평균으로 대체
for col in with_zeros :
    df[col] = df[col].fillna(df[col].mean())

df.head()

# 이상치 처리
# 상위 1%를 이상치로 간주하고 평균으로 대체
outliers_col = ['SkinThickness', 'Insulin']
for col in outliers_col :
    threshold = df[col].quantile(0.99)      # 상위 1% -> 하위 99% 경계값
    without_threshold_mean = df[df[col] <= threshold][col].mean()       # 상위 1%를 제외한 평균
    df.loc[df[col] > threshold, col] = without_threshold_mean           # 제외한 평균으로 대체

# 정규화
scaler = MinMaxScaler()
df['Age'] = scaler.fit_transform(df[['Age']])

# EDA == 탐색적 데이터 분석
# 각 열의 결측치 개수 출력
print('각 열의 결측치 개수 : ')
print(df.isnull().sum())
print('='*50)
print()

# Outcome 별 Glucose 평균 출력
print('Outcome 별 Glucose 평균 : ')
print(df.groupby('Outcome')['Glucose'].mean())
print('='*50)
print()

# 전처리 후 데이터프레임 상위 5개 행 출력
print('데이터프레임 상위 5개 : ')
print(df.head())
print('='*50)
print()