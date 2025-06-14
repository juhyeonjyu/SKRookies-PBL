import os
import re
import time

"""
디렉터리 감시를 통한 보안 위협 탐지
특정 파일 생성과 민감 정보 포함 여부를 실시간으로 감지하고 분석합니다.

시스템 보안을 위해 특정 디렉터리에 새로운 파일이 생성되는지 모니터링해야 하며, 보안 위험이 될 수 있는 파일과 내용을 탐지해야 합니다.
"""

# 파일 초기 목록 확인 메서드
def initial_file_list() :
    try :
        return os.listdir('./monitor_directory')
    except Exception as e :
        print(f'초기 파일 목록 확인 중 오류 : {e}')
        return []

# 새로 생긴 파일 탐지 및 출력 메서드
def check_new_file(before_files) :
    try :
        after_files = os.listdir('./monitor_directory')
    except Exception as e :
         print(f'디렉터리 접근 중 오류 : {e}')
         return []
    
    new_files = set(after_files) - set(before_files)
    if new_files :
        print('새로 생긴 파일 : ', new_files)
    return list(new_files)

# 위험할 수 있는 확장자 (.py, .js, .class) 파일 탐지 시 경고 메세지 출력 메서드
def check_danger_exts() :
    danger_files = []
    try :
        for file in os.listdir('./monitor_directory') :
            _, file_type = os.path.splitext(file)
            if file_type in ['.py', '.js', '.class'] :
                print(f'위험할 수 있는 파일이 발견되었습니다. : {file}')
                danger_files.append(file)
    except Exception as e :
         print(f'위험 파일 탐지 중 오류 : {e}')
    return danger_files

# 민감 정보(주석, 이메일, SQL문) 탐지 시 출력 메서드
def check_sensitive_data(file_list) :
    for file in file_list :
        path = os.path.join('./monitor_directory', file)
        try :
            with open(path, 'r', encoding='UTF8') as f :
                text = f.read()
        except Exception as e :
            print(f'[오류] {file} 파일 열기 실패 : {e}')
            continue
        
        found_danger =[]
        if re.search(r'(/\*[\s\S]*?\*/|//.*|#.*)', text) :
                found_danger.append('주석')
        if re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text) :
                found_danger.append('이메일')
        if re.findall(r'\b(select|insert|update|delete)\b', text, re.IGNORECASE) :
                found_danger.append('SQL문')

        if found_danger :
            print(f'{file} 내 포함된 민감 정보 : {", ".join(found_danger)}')
        else :
             print(f'{file} : 민감 정보 없음')

# 실시간 모니터링 실행 메서드
def monitoring_execution() :
    print('-'*10, '실시간 모니터링을 시작합니다.', '-'*10)

    checked_files = initial_file_list()
    danger_files = check_danger_exts()
    check_sensitive_data(danger_files)

    while True :
        time.sleep(3)
        new_files = check_new_file(checked_files)
        if new_files :
            for f in new_files :
                 if f not in checked_files :
                      checked_files.append(f)
            check_sensitive_data(new_files)

monitoring_execution()