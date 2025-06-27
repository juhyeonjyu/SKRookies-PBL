import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

"""
OpenAI 함수 호출 기능 활용 AI Agent 구현
Chat GPT API 활용 및 Function Calling 흐름 설계

최근 OpenAI의 GPT-4 모델에는 대화 중 함수 호출(Function Calling) 기능이 추가되어, 사용자의 요청을 외부 함수로 처리할 수 있는 구조를 지원하고 있습니다.
이 기능은 계산, 날짜 변환, 검색 등 명확한 작업을 코드 수준에서 처리하고 결과만 대화에 반영할 수 있게 하여, 챗봇의 정확성과 활용도를 크게 높이고 있습니다.
이 기능을 활용하여, 날짜 형식 변환 및 덧셈 요청을 자동으로 처리할 수 있는 AI 에이전트를 구현합니다.

사용자가 자연어로 요청하면 모델이 적절한 함수를 선택하여 호출하고, 그 결과를 다시 자연어로 응답합니다.
"""

class OpenAIAgent :
    def __init__(self): 
        # OpenAI API 키 설정
        load_dotenv()
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=OPENAI_API_KEY)

        # 함수 정의
        self.tools = [{
            'type' : 'function',
            'name' : 'convert_date_format',
            'description' : '날짜 문자열을 다른 형식으로 변환합니다.',
            'parameters' : {
                'type' : 'object',
                'properties' : {
                    'date' : {
                        'type' : 'string', 'description' : '기존 입력 날짜 형식 : YYYY년 MM월 DD일'
                    },
                    'output' : {
                        'type' : 'string', 'description' : '변환할 날짜 형식'
                    }
                },
            },
            'required': ['date', 'output']
        }, {
            'type' : 'function',
            'name' : 'add_numbers',
            'description' : '두 숫자를 더합니다.',
            'parameters' : {
                'type' : 'object',
                'properties' : {
                    'x' : {
                        'type' : 'number', 'description' : '첫 번째 숫자'
                    },
                    'y' : {
                        'type' : 'number', 'description' : '두 번째 숫자'
                    }
                },
            },
            'required': ['x', 'y']
        }]

    # 날짜 문자열을 다른 형식으로 변환하는 함수
    def convert_date_format(self, date, output) :
        temp = datetime.strptime(date, '%Y년 %m월 %d일')
        return temp.strftime(output)

    # 두 숫자를 더하는 함수
    def add_numbers(self, x, y) :
        return x + y
    
    def run(self) :
        # 사용자 프롬프트 입력
        query = input('무엇을 도와드릴까요? : ')
        messages = [{ 'role' : 'user', 'content' : query }]
        input_msg = messages[:]

        # 1차 응답 : 함수 호출 여부 판단
        response = self.client.responses.create(
            model = 'gpt-4.1',
            input = query,
            tools = self.tools
        )

        # 함수 호출 있을 시 처리
        if response.output :
            for tool_call in response.output :
                if tool_call.type == 'function_call' :
                    # 매개변수 추출
                    args = json.loads(tool_call.arguments)
                    if tool_call.name == 'convert_date_format':
                        result = self.convert_date_format(args['date'], args['output'])
                    elif tool_call.name == 'add_numbers':
                        result = self.add_numbers(args['x'], args['y'])
                    else:
                        continue  # 정의되지 않은 함수는 무시

                    print(f"[함수 호출 결과] {tool_call.name} 실행 → {result}")

                    input_msg.append(tool_call)
                    input_msg.append({
                        'type': 'function_call_output',
                        'call_id': tool_call.call_id,
                        'output': str(result)
                    })
                            
        # 최종 응답 생성
        response_msg = self.client.responses.create(
            model='gpt-4.1',
            input=input_msg,
            tools=self.tools
        )
        print(response_msg.output_text)

if __name__ == '__main__' :
    agent = OpenAIAgent()
    agent.run()