import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

# URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

# #body-content > div.newest-list > div > table > tbody > tr
musics = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

# movies (tr들) 의 반복문을 돌리기
for music in musics:
    # 순위: td.number
    number = music.select_one('td.number').text
    rank = [int(i) for i in number.split() if i.isdigit()]
    # 곡명: td.info > a.title.ellipsis
    name = music.select_one('td.info > a.title.ellipsis').text
    strip_name = name.strip()
    # 가수: td.info > a.artist.ellipsis
    artist = music.select_one('td.info > a.artist.ellipsis').text
    lists = {
            'rank' : rank[0],
            'name' : strip_name,
            'artist' : artist
        }
    print(lists)
    db.musics.insert_one(lists)