import requests
from urllib import parse
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, render_template
from typing import List
from pymongo import MongoClient
from collections import OrderedDict

app = Flask(__name__)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.uploaded                      # 'dbsparta'라는 이름의 db를 만듭니다.


@app.route('/')
def index():
    return render_template('kakao.html')


@app.route('/upload', methods = ['POST'])
def upload():
    file = request.files.getlist('file[]')  # file[]는 FileList인 상태
    f = []
    for x in file:
        x = x.read()  # x는 FileStroage인 상태. read로 읽어 bytes로 풀어준다.
        x = x.decode('utf-8')  # x는 bytes로 풀린 상태. 우리가 인식할 수 있게 utf-8로 str형태로 만들어준다.
        f.append(x)  # 변환된 str을 리스트로 만든다. 각각의 리스트는 하나의 txt파일의 모든 내용물을 의미함.

    # 작업에 앞서 db를 초기화한다.
    if 'dialogue' in db.list_collection_names():
        db.dialogue.drop()

    # 몇 개의 txt 파일이나 불러왔지? 정제 활동을 txt파일의 갯수만큼 반복하려한다.
    file_len = len(f)
    dialogue = []

    for i in range(file_len):
        contents_list = f[i].split('\r\n')

        # 상위 3개 lines 제거
        for a in range(3):
            del contents_list[0]

        # 날짜 표시선 제거
        for x in contents_list:
            if '---' in x:
                contents_list.remove(x)

        # [사람이름] [오전 시간:시간] 항목을 제거해서 순수한 대화 내용 텍스트만 남깁니다 = dialogue: list
        for x in contents_list:
            for a in range(2):
                d = x.find(']')
                x = x[d + 2:]
            dialogue.append({"comment": x})

        [dialogue.append({"comment": 0}) for e in range(10)]

        # dialogue 를 db에 저장하기
        print(dialogue)
        db.dialogue.insert(dialogue)

    return jsonify({'result': 'success', 'result_list': dialogue})


@app.route('/search', methods=['GET'])
def search():
    # 원하는 검색어를 받기. 브라우저에서 요청하는 검색어는 'word_search'로 약속.
    to_search = request.args.get('word_search')

    # naver api 주소
    api = 'https://openapi.naver.com/v1/search/cafearticle.json?query='

    # 한글을 url 에 넣기 위하여 검색어를 utf-8 형식으로 변환합니다.
    s_text = parse.quote(to_search)

    # naver api 에 요청하기 위한 url을 작성합니다. (조립 과정)
    conditions = '&display=100&start=1&sort=sim'
    url_list = [api, s_text, conditions]
    url = ''.join(url_list)
    print(url)

    # header 에서는 naver api 에서 준 아이디, 비번 키-밸류// 크롤링을 위한 bs4용 유저 에이전트 키-밸류를 넣습니다.
    headers = {'X-Naver-Client-Id': 'U2HktS4ang1cWLc3MVUK',
               'X-Naver-Client-Secret': '_TiVT3vAcI',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36\
               (KHTML, like Gecko)Chrome/73.0.3683.86 Safari/537.36'}

    # 네이버 오픈 api 에 카페 검색 정보를 달라고 GET 요청합니다.
    # 돌아오는 key: cafename, cafeurl, description, link, title
    r = requests.get(url, headers=headers)
    rjson = r.json()  # json 으로 변환했는데 왜 list 로 읽히는지... 모르겠음
    ritems = rjson['items']

    # 리스트-딕셔너리 구조에서 딕셔너리의 키값이 'cafeurl' 인 것들만 빼내기 위한 함수입니다.
    def search(name, people):
        return [element for element in people if element['cafeurl'] == name]

    # 딕셔너리에서 카페 주소를 긁어옵니다.
    sritems = search('https://cafe.naver.com/sevenknights', ritems)
    link_list = []
    length = len(sritems)

    # link_list 는 네이버 카페의 원하는 글 링크를 담은 리스트입니다.
    for i in range(length - 1):
        link_list.append(sritems[i]['link'])

    # 인터넷 카페 환경은 크롤링하기 어려운 구조로 되어있어 모바일 카페 환경에서 진행합니다.
    for i in range(length - 1):
        link_list[i] = link_list[i].replace('http://cafe', 'http://m.cafe')

    result_list = []
    dialogue_search = []

    # link 들의 list 를 모두 돌리면서 제목, 내용, 댓글[1]~[n]로 크롤링하여 모든 글을 리스트로 만듭니다.
    for i in range(length - 1):
        data = requests.get(link_list[i], headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')

        # 글 제목을 저장합니다.
        title = soup.select_one('title').text.replace(' : 네이버 카페', '')

        # 글 내용을 저장합니다.
        contents = soup.select('#postContent > p')
        content_list = []
        [content_list.append(content.get_text().strip()) for content in contents]
        content = ''.join(content_list)

        # 댓글은 여러개니까 이를 리스트로 저장합니다.
        comments = soup.select('#commentArea > div.section_comment > ul p')
        comment_list = []
        [comment_list.append(comment.get_text().strip()) for comment in comments]
        comment_col = ' // '.join(comment_list).splitlines()
        comment_col = [w.replace('\t', '') for w in comment_col]
        comment_col = ''.join(comment_col).split(' // ')
        comment_col = '<br>'.join(comment_col)

        result_list.append({'title': title, 'content': content, 'comment_col': comment_col})

    # db에서 카카오톡 대화 내역 불러오기
    dialogue_com = list(db.dialogue.find({}, {"_id": 0}))
    dialogue = [d['comment'] for d in dialogue_com]
    print(dialogue)

    # 해당 검색어가 포함된 대화내용 및 이후 10개 대화내용까지 저장.
    for x in dialogue:
        if to_search in str(x):
            n = dialogue.index(x)
            for a in range(10):
                dialogue_search.append(dialogue[n + a])

    # 중복 대화값을 제거하여 대화 내용 리스트를 만듭니다. (서버에 리턴되는 리스트임)
    dia_kakao = list(OrderedDict.fromkeys(dialogue_search))
    print(dia_kakao)
    result_list.append({'kakao': dia_kakao})

    # result_list 를 반환합니다.
    return jsonify({'result': 'success', 'result_list': result_list})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)