import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
과목별 성적 분석을 통한 학생 성과 시각화
난수 기반 성적 데이터를 활용한 통계 분석 및 시각화

20명의 학생의 과목별 성적 데이터를 분석하여 통계적 인사이트를 시각적으로 제공하고자 합니다.
"""

# 클래스 정의
class StudentScoreAnalysis :
    # 생성자 메서드
    def __init__(self) :
        # 학생 이름
        students = []
        for i in range(0, 20) :
            students.append('학생'+str(i+1))
        self.name = students
        # 수학, 영어, 과학 점수
        self.math = np.random.randint(50, 101, size=len(students))
        self.eng = np.random.randint(50, 101, size=len(students))
        self.science = np.random.randint(50, 101, size=len(students))
        # 데이터프레임 생성
        self.df = pd.DataFrame({
            'name' : self.name,
            'math' : self.math,
            'eng' : self.eng,
            'science' : self.science
        })
    
    # 과목별 평균 계산 메서드
    def cal_sub_avg(self) :
        math_avg = self.df['math'].mean()
        eng_avg = self.df['eng'].mean()
        science_avg = self.df['science'].mean()

        return {'수학': math_avg, '영어': eng_avg, '과학': science_avg}

    # 학생별 평균 계산 및 정렬 메서드
    def stu_avg_sort(self) :
        self.df['st_avg'] = self.df[['math', 'eng', 'science']].mean(axis=1)
        top_stu = self.df.set_index('name')['st_avg'].sort_values().head(5)
        return top_stu

    # 과목별 평균 시각화 메서드
    def sub_avg_graph(self) :
        sub_avg = self.cal_sub_avg()
        plt.rc('font', family='Malgun Gothic')
        plt.barh(list(sub_avg.keys()), list(sub_avg.values()),
                 color='green',
                 edgecolor='black'
        )
        plt.title('Subject Averages')
        plt.ylabel('Subject')
        plt.xlabel('Average')
        plt.show()

    # 평균 성적 상위 5명 시각화 메서드
    def top_stu_graph(self) :
        top_stu = self.stu_avg_sort()
        plt.rc('font', family='Malgun Gothic')
        plt.barh(top_stu.index, top_stu.values,
                 color='green',
                 edgecolor='black'
        )
        plt.title('Top 5 Students')
        plt.ylabel('Student name')
        plt.xlabel('Score')
        plt.show()

test = StudentScoreAnalysis()
test.sub_avg_graph()
test.top_stu_graph()