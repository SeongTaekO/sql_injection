import re
import pandas as pd
import urllib.parse

# 로그 파일 읽기
with open("c:/Users/user/Downloads/access.log", "r") as fd:
    data = fd.read()

# 엑셀 파일 초기화
output_file_path = "SQLinjection___.csv"
columns = ["injection", "공격 유형", "설명", "탐지 정규식"]
df = pd.DataFrame(columns=columns)

types = ['논리적 조건 조작', 'UNION 기반 정보 검색', '데이터 길이 기반 조건 검색']

descs = [
    "논리적 조건을 항상 참으로 만들어 인증 우회", 
    "Column 수를 알아내려고 시도",
    "현재 사용 중인 데이터베이스의 이름을 알아내려고 시도",
    "table_name에 대한 정보를 얻으려고 시도",
    "column_name에 대한 정보를 얻으려고 시도",
    "컬럼의 길이를 알아내려고 시도"
]

# 정규 표현식 패턴 정의 (공백이나 + 기호를 포함)
patterns = [
    re.compile(r"(\d)*?'\s*?or\s(1=1|true|\'\d*\'=\'\d*\')", re.IGNORECASE),
    re.compile(r"(\d)*?\'\s*?union\sselect\s(\d+\s*?\,\s*?)*\d+\s*?(#)", re.IGNORECASE),
    re.compile(r"(\d)*?\'\s*?union\sselect\s(\d*?\s*?\,\s*?)*\d*?\s*?database\(\)", re.IGNORECASE),
    re.compile(r"(\d)*?\'\s*?union\sselect\s(\d*?\s*?\,\s*?)*\d*?\s*?table_name\s(\d*?\s*?\,\s*?)*\d*?\s*?from\sinformation_schema\.tables\s(where\stable_schema\s*?\=\s*?\'(.*)\')*?", re.IGNORECASE),
    re.compile(r"(\d)*?\'\s*?union\sselect\s(\d*?\s*?\,\s*?)*\d*?\s*?column_name", re.IGNORECASE),
    re.compile(r"(\d)*?\'\s*?and\s\(select\s\d\sfrom\sinformation_schema\.columns\swhere\stable_schema\=\'(.*)\'(\sand\stable_name\=\'(.*)\')*?(\sand\slength\(column_name\)\=\d)*?", re.IGNORECASE),

]

for line in data.split("\n"):
    if len(line) == 0:
        continue
    match = re.match(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s\-\s\-\s\[(.+)\]\s\"(GET|POST|OPTIONS)\s(.+)\sHTTP\/\d\.\d\"\s(\d{3})\s(\-|\d+)\s\"(.*)\"\s\"(.+)\"', line)
    if match:
        ip, datetime, method, uri, status_code, data_size, referer, ua = match.groups()
        for i in range(0, len(patterns)):
            decoded_uri = urllib.parse.unquote(uri)
            decoded_uri = decoded_uri.replace('+', ' ')
            decoded_uri = decoded_uri.lower()
            if re.search(patterns[i], decoded_uri):
                
                # 31번째 문자부터 '#'가 나타날 때까지 부분 문자열 추출
                injection_start = 31
                injection_end = decoded_uri.find('#', injection_start)
                if injection_end == -1:
                    injection_end = len(decoded_uri)
                injection = decoded_uri[injection_start:injection_end+1]
                
                if i == 0:
                    type = types[0]
                elif i >= 1:
                    type = types[1]
                desc = descs[i]

                # 데이터 프레임에 행 추가
                df = df._append({
                    "injection": injection,
                    "공격 유형": type,
                    "설명": desc,
                    "탐지 정규식": patterns[i]
                }, ignore_index=True)
                
                break

# 엑셀 파일 저장
df.to_csv(output_file_path, index=False)

