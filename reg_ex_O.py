import re, pandas as pd
from urllib.parse import unquote


def main():
    with open("C:\\Users\\ost09\\OneDrive\\바탕 화면\\다크웹 크롤러\\access2.log", "r") as f:
        data = f.read()

    pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s\-\s\-\s\[(.+)\]\s\"(GET|OPTIONS|POST)\s(.+?)(id=.+?)?(Submit=.+?)?\s(HTTP\/\d\.\d)\"\s(\d{3})\s(\d+|\-)\s\"(.+|\-)\"\s\"(.+|\-)\""
    pattern_TRUE = r"(?i)id=(\d+\'|\')\sOR\s(\d\=\d|\'\d\'\=\'\d\'|TRUE)\s(LIMIT\s\d\s)?\#"
    pattern_UNION_SELECT_get_columns_num = r"(?i)id=(\d+\'|\')\sUNION\sSELECT\s(?:\d+(?:,\s\d+){0,9})?\s\#"
    pattern_UNION_SELECT_get_table_name = r"(?i)id=(\d+\'|\')\sUNION\sSELECT\s(\d\,(\w+|\s\w+)|\w+\,\s\d)\sFROM\s\w+\.\w+\s(WHERE\s\w+\=\'\w+\'\s)?\#"
    pattern_UNION_SELECT_get_data = r"(?i)id=\d*'\sUNION\sSELECT\s(?:\w+(?:,\s*\w+)*|\d+(?:,\s*\d+)*)(?:\sFROM\s(?:\w+\.)?\w+)?(?:\sWHERE\s.+?)?(?:\sLIMIT\s\d+,\d+)?\s*#"
    pattern_DB_NAME = r"(?i)database\(\)"
    pattern_COLUMN_LEN = r"(?i)LENGTH\("
    pattern_COLUMN_NAME = r"(?i)UNION\sSELECT(.+)information_schema.columns\sWHERE(.+)(LIMIT)?"

    df = pd.DataFrame(columns=["ip", "date", "method", "uri", "payload", "injection_format"])
    i = 1
    
    for line in data.split("\n"):
        if len(line) == 0:
            continue

        matches = re.match(pattern, line)

        id = unquote(matches[5]).replace("+", " ")
        submit = unquote(matches[6]).replace("+", " ")

        # with open("output.txt", "a") as f:
        #     if id == "id=&" and submit == "Submit=Submit":
        #         continue
        #     f.write(f"{id}{submit}\n")
        #     f.write(f"{matches[5]}{matches[6]}\n")

        injection_format = ""

        if re.match(pattern_TRUE, id):   
            print(str(i),":", id)
            injection_format = "조건문 우회"
            i += 1
        elif re.match(pattern_UNION_SELECT_get_columns_num, id):
            print(str(i),":", id)
            injection_format = "UNION SELECT: DB의 컬럼개수"
            i += 1
        elif re.match(pattern_UNION_SELECT_get_table_name, id):
            print(str(i),":", id)
            injection_format = "UNION SELECT: 테이블 이름"
            i += 1
        elif re.match(pattern_UNION_SELECT_get_data, id):
            print(str(i),":", id)
            injection_format = "UNION SELECT: 컬럼에 저장된 값"
            i += 1
        elif re.search(pattern_DB_NAME, id):    
            print(str(i),":", id)
            injection_format = "DB 이름"
            i += 1
        elif re.search(pattern_COLUMN_LEN, id):   
            print(str(i),":", id)
            injection_format = "컬럼 길이"
            i += 1
        elif re.search(pattern_COLUMN_NAME, id):    
            print(str(i),":", id)
            injection_format = "컬럼 이름"
            i += 1
        else:
            print(id)
        
        df.loc[len(df)] = [matches[1], matches[2], matches[3], matches[4], id+submit, injection_format]
    df.to_csv("output.csv", index=False)


if __name__ == "__main__":
    main()