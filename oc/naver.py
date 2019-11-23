import requests
from urllib import parse
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from typing import List
app = Flask(__name__)


@app.route('/search', methods = ['GET'])
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

    # link 들의 list 를 모두 돌리면서 제목, 내용, 댓글[1]~[n]로 크롤링하여 모든 글을 리스트로 만듭니다.
    for i in range(length - 1):
        data = requests.get(link_list[i], headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')

        # 글 제목을 저장합니다.
        title = soup.select_one('title').text.replace(' : 네이버 카페', '')

        # 글 내용을 저장합니다.
        contents = soup.select('#postContent > p')
        content_list = []
        [content_list.append(content.get_text().strip().replace('<br>', '')) for content in contents]
        content = ''.join(content_list)

        # 댓글은 여러개니까 이를 리스트로 저장합니다.
        comments = soup.select('#commentArea > div.section_comment > ul p')
        comment_list = []
        [comment_list.append(comment.get_text().strip()) for comment in comments]
        comment_col = ' // '.join(comment_list).splitlines()
        comment_col = [w.replace('\t', '') for w in comment_col]
        comment_col = ''.join(comment_col).split(' // ')

        result_list.append({'title': title, 'content': content, 'comment_col': comment_col})

    # result_list 를 반환합니다.
    return jsonify({'result': 'success', 'result_list': result_list})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)