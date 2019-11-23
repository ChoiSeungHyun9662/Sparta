import requests
import pprint

api = 'https://openapi.naver.com/v1/search/cafearticle.json?query='
b_text = str(b, 'utf-8')
print(b_text)
conditions = '&display=2&start=1&sort=sim'
url_list = [api, "s_text", conditions]
url = ''.join(url_list)
print(url)

headers = {'X-Naver-Client-Id': 'U2HktS4ang1cWLc3MVUK', 'X-Naver-Client-Secret': '_TiVT3vAcI'}
r = requests.get('https://openapi.naver.com/v1/search/cafearticle.json?query=%EC%A3%BC%EC%8B%9D&display=2&start=1&sort=sim', headers=headers)
rjson = r.json()
pprint.pprint(rjson)