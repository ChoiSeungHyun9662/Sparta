from collections import OrderedDict
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('kakao.html')

@app.route('/search', methods=['POST'])
def search2():
    # 모든 텍스트 파일을 불러와서 저장
    # <form method="post" enctype="multipart/form-data">
    #             <input type="file" name="files[]" multiple>
    #             <input type="submit" value="Upload">
    #         </form>
    files = request.files.getlist("files[]")

    #file_read는 textfile을 python에서 open한 결과를 받는 리스트.
    file_read = []
    f = open(files[0], 'r', encoding="utf-8")
    if f.mode == 'r':
        file_read = file_read.append(f.read())

    # 스트링을 리스트로 만들자
    contents_list = file_read[0].split('\n')

    # 상위 3줄 및 날짜 표시 줄 제거
    for i in range(3):
        del contents_list[0]

    for x in contents_list:
        if '---' in x:
            contents_list.remove(x)
    print(contents_list)

    # [사람이름] [오전 시간:시간] 항목을 제거해서 순수한 대화 내용 텍스트만 남깁니다. 이를 dialogue list로 저장.
    dialogue = []
    for x in contents_list:
        for i in range(2):
            d = x.find(']')
            x = x[d + 2:]
        dialogue.append(x)

    print(dialogue)

    # 원하는 검색어를 받기
    to_search = request.args.get('word_search')

    # 해당 검색어가 포함된 대화내용 및
    dialogue_2 = []
    for x in dialogue:
        if to_search in x:
            n = dialogue.index(x)
            for i in range(10):
                dialogue_2.append(dialogue[n + i])

    # 중복 대화값을 제거하여 대화 내용 리스트를 만듭니다. (서버에 리턴되는 리스트임)
    dia_kakao = list(OrderedDict.fromkeys(dialogue_2))
    print(dia_kakao)

    return jsonify({'result': 'success', 'result_list': dia_kakao})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)