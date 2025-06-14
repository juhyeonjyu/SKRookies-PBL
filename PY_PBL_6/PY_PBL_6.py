import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
고객 구매 데이터를 활용한 매출 및 기여도 분석
월별 매출과 고객별 누적 기여도 시각화

고객의 구매 데이터를 기반으로 마케팅 전략 수립을 위한 월별 매출 및 고객별 누적 기여도 분석이 필요합니다.
"""

class CustomerSalesAnalysis :
    # 생성자 메서드
    def __init__(self):
        # 고객명
        customers = []
        for i in range(0, 15) :
            customers.append('고객'+str(i+1))
        self.name = customers
        # 구매일자
        date = pd.date_range(start="2024-01-01", end="2024-12-31", freq='D')
        self.date = np.random.choice(date, size=len(customers))
        # 상품명
        self.product = np.random.choice(['사과', '딸기', '복숭아', '수박', '오렌지'], size=len(customers))
        # 수량
        self.amount = np.random.randint(1, 11, size=len(customers))
        # 단가
        self.price = np.random.randint(1000, 25001, size=len(customers))
        # 데이터프레임 생성
        self.df = pd.DataFrame({
            'name' : self.name,
            'date' : self.date,
            'product' : self.product,
            'amount' : self.amount,
            'price' : self.price
        })
        # 총매출 파생열 생성
        self.df['sales'] = self.df['amount'] * self.df['price']

    # 월별 매출 계산 메서드
    def monthly_sales(self) :
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df['month'] = self.df['date'].dt.to_period('M')
        monthly_sales = self.df.groupby('month')['sales'].sum()

        return monthly_sales           

    # 월별 매출 시각화
    def monthly_sales_graph(self) :
        monthly = self.monthly_sales()
        plt.rc('font', family='Malgun Gothic')
        plt.bar(monthly.index.astype(str), monthly.values,
                    color='green',
                    edgecolor='black'
        )
        plt.title('월별 매출 그래프')
        plt.xlabel('월')
        plt.ylabel('매출 총합')
        plt.show()

    # 고객별 누적 매출 계산 메서드
    def total_sales(self) :
        total_sales = self.df.groupby('name')['sales'].sum()
        return total_sales

    # 고객별 누적 매출 시각화
    def total_sales_graph(self) :
        total = self.total_sales()
        plt.rc('font', family='Malgun Gothic')
        plt.pie(total.values, labels=total.index, autopct='%.1f%%')
        plt.title('고객별 누적 매출 차트')
        plt.show()

test = CustomerSalesAnalysis()
print('월별 매출 총합 : ', test.monthly_sales())
test.monthly_sales_graph()
print('고객별 누적 매출 : ', test.total_sales())
test.total_sales_graph()