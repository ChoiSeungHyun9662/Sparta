import requests # requests 라이브러리 설치 필요
import pprint

r = requests.get('http://openapi.seoul.go.kr:8088/6d4d776b466c656533356a4b4b5872/json/RealtimeCityAir/1/99')
rjson = r.json()
row = rjson['RealtimeCityAir']['row']

for order in row:
    region = order['MSRSTE_NM']
    if region == '중구':
        print(order['NO2'])