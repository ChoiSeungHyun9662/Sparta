from collections import OrderedDict
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('kakao.html')

@app.route('/search', methods=['POST'])
def search2():
    file = request.files.getlist('file[]')  # file[]는 FileList인 상태
    f = []
    for x in file:
        x = x.read()  # x는 FileStroage인 상태. read로 읽어 bytes로 풀어준다.
        x = x.decode('utf-8')  # x는 bytes로 풀린 상태. 우리가 인식할 수 있게 utf-8로 str형태로 만들어준다.
        f.append(x)  # 변환된 str을 리스트로 만든다. 각각의 리스트는 하나의 txt파일의 모든 내용물을 의미함.

    # 몇 개의 txt 파일이나 불러왔지? 정제 활동을 txt파일의 갯수만큼 반복하려한다.
    file_len = len(f)
    dialogue_search = []

    for i in range(file_len):
        contents_list = f[i].split('\r\n')

        # 상위 3개 lines 제거
        for a in range(3):
            del contents_list[0]

        # 날짜 표시선 제거
        for x in contents_list:
            if '---' in x:
                contents_list.remove(x)
        print(contents_list)

        # [사람이름] [오전 시간:시간] 항목을 제거해서 순수한 대화 내용 텍스트만 남깁니다 = dialogue: list
        dialogue = []
        for x in contents_list:
            for a in range(2):
                d = x.find(']')
                x = x[d + 2:]
            dialogue.append(x)

        [dialogue.append('') for e in range(10)]

        print(dialogue)

        # 원하는 검색어를 받기
        to_search = '할노부'  # request.args.get('word_search')

        # 해당 검색어가 포함된 대화내용 및 이후 10개 대화내용까지 저장.
        for x in dialogue:
            if to_search in x:
                n = dialogue.index(x)
                for a in range(10):
                    dialogue_search.append(dialogue[n + a])

    # 중복 대화값을 제거하여 대화 내용 리스트를 만듭니다. (서버에 리턴되는 리스트임)
    dia_kakao = list(OrderedDict.fromkeys(dialogue_search))
    dia_kakao.remove('')
    print(dia_kakao)

    return jsonify({'result': 'success', 'result_list': dia_kakao})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)