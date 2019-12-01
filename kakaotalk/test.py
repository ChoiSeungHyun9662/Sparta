from collections import OrderedDict
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('kakao.html')

@app.route('/search', methods=['POST'])
def search2():
    # 모든 텍스트 파일을 불러와서 저장
    file = request.files.getlist('file[]')  # file[]는 FileList인 상태
    print(type(file[0]))
    f = []
    for x in file:
        x = x.read()  # x는 FileStroage인 상태. read로 읽어 bytes로 풀어준다.
        x = x.decode('utf-8')  # x는 bytes로 풀린 상태. 우리가 인식할 수 있게 utf-8로 str형태로 만들어준다.
        f.append(x)  # 변환된 str을 리스트로 만든다. 각각의 리스트는 하나의 txt파일의 모든 내용물을 의미함.

    len1 = len(f)
    print(len1)

    return jsonify({'result': 'success', 'result_list': f})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)