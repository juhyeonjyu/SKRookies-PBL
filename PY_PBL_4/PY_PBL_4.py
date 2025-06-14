import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
계열 매출 데이터를 활용한 월별 매출 분석
Pandas와 Matplotlib을 활용한 연간 매출 추이 시각화

1년간의 매출 데이터를 분석하여 월별 매출 추이를 시각화해 비즈니스 인사이트를 도출하고자 합니다.
"""

class SalesAnalysis :
    # 생성자 메서드
    def __init__(self):
        # 날짜 생성
        self.dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq='D')
        # 매출 난수 생성
        self.sales = np.random.randint(1000, 10001, size=len(self.dates))
        self.df = pd.DataFrame({
            'date' : self.dates,
            'sales' : self.sales
        })

    # 월별 매출 집계 및 출력 메서드
    def monthly_sales(self) :
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df['month'] = self.df['date'].dt.to_period('M')
        monthly_sales = self.df.groupby('month')['sales'].sum()
        print(monthly_sales)
        return monthly_sales
    
    # 시각화 메서드
    def graph(self) :
        monthly = self.monthly_sales()
        plt.rc('font', family='Malgun Gothic')
        plt.plot(monthly.index.astype(str), monthly.values,
                 marker='o',
                 linestyle='-',
                 color='green',
                 label='Sales'
        )
        plt.title('Monthly Sales')
        plt.xlabel('Month')
        plt.ylabel('Total')
        plt.legend()
        plt.grid()
        plt.show()

sales_anly = SalesAnalysis()
sales_anly.graph()