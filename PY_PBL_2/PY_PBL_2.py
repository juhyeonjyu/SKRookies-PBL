import os
import re
from collections import Counter
import csv

"""
로그 파일을 활용한 IP 접속 분석
정규 표현식과 데이터 구조를 이용한 접속 IP 분석

서버 보안 분석을 위해 로그 파일에서 접속한 IP 주소를 파악해야 하며, 이를 통해 자주 접속한 IP를 분석하고 보고해야 합니다.
"""

log_path = input('로그 파일 경로를 입력해 주세요 : ')

# 로그 파일 경로 존재 여부 확인
def path_check() :
    try :
        if os.path.exists(log_path) is False :
            print('로그 파일 경로를 찾을 수 없습니다. 다시 시도해 주세요.')
        return log_path
    except FileNotFoundError as e :
        print(e)
        exit()

# 경로 내 로그 파일 존재 여부 확인 후 파일 절대경로 반환
def file_check() :
    try :
        path = path_check()
        f_list = os.listdir(path)

        log_files = [file for file in f_list if file.endswith(".log")]
        if not log_files :
            raise FileNotFoundError('로그 파일이 존재하지 않습니다.')
        
        return os.path.join(path, log_files[0])
    except FileNotFoundError as e :
        print(e)
        exit()


# IP 주소 추출
def get_ip_adds(log_file_path) :
    with open(log_file_path, 'r', encoding='UTF8') as f :
        text = f.read()
        ip_adds = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)
    return ip_adds

# IP 주소 빈도 계산
def get_ip_counts(ip_list) :
    return Counter(ip_list)

# 상위 3개 IP 주소 출력
def get_three_top_counts_ip(ip_counter) :
    return ip_counter.most_common(3)

# 분석 결과 CSV 저장
def save_as_csv(ip_counter) :
    with open('ip_analysis.csv', 'w', encoding='utf-8-sig', newline='') as f :
        data = csv.writer(f)
        data.writerow(['IP Address', 'Count'])
        for ip, count in ip_counter.items() :
            data.writerow([ip, count])

log_file = file_check()
ip_list = get_ip_adds(log_file)
ip_counter = get_ip_counts(ip_list)

save_as_csv(ip_counter)

print('상위 3개 IP 주소: ')
for ip, count in get_three_top_counts_ip(ip_counter) :
    print(f'{ip} = {count}회')