import requests
import pprint
import codecs

api = 'https://openapi.naver.com/v1/search/cafearticle.json?query='
with codecs.open('search.txt', 'r', encoding='utf8') as f:
    s_text = f.read()
print(s_text)
b = '콜트'
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