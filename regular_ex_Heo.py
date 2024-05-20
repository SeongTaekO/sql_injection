import re
import pandas

db = {
    "union": "union 기반 정보 검색",
    "select \d+(\s*,\s*\d+)+" : "컬럼 갯수 검색",
    "select 1" : "컬럼 갯수 검색",
    "select.*database()" : "데이트 베이스 검색",
    "select.*table_name.*from\s*information_schema.tables" : "테이블 이름들 검색",
    "select.*column_name.*from\s*information_schema.columns" : "컬럼 이름들 검색",
    "select.*from.*where.*length\(.*\)" : "특정 컬럼 이름 길이 검색",
    "or\s+('1'='1'|true|1=1)" : "or 기반 정보 검색",
    "select.*from\s*\S*\s*" : "%s 테이블에 %s 컬럼 추출"
}
logs = "sdf"
with open("./target.txt", "rt") as f:
    logs = f.readlines()
    # print(logs)
    
result = {"ip" : [], "logs" : [], "date" : [], "comment" : []}
for log in logs :
    result["comment"].append([])
    for key, value in db.items():
        if re.search(key, log):
            if key == "select.*from\s*\S*\s*" :
                result["comment"][-1].append(value % (re.search("from\s*(\S*)\s*", log).group(1) , re.search("select\s*(.*)\s*from", log).group(1) ))
                continue
            result["comment"][-1].append(value)
            
    result["ip"].append(log.split(" ")[0])
    result["date"].append(log.split(" ")[3])
    result["logs"].append(log.split(" ")[7])

            

df = pandas.DataFrame(result)
df.to_csv("output.csv", index=False, encoding="cp949")

