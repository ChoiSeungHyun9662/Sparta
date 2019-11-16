from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

@app.route('/')
def home():
   return render_template('OnePageShoppingMall.html')

@app.route('/order', methods=['GET'])
def listing():
    # item_give 클라이언트가 준 item를 가져오기
    item_receive = request.args.get('item_give')
    # item의 값이 받은 item와 일치하는 document 찾기 & _id 값은 출력에서 제외하기
    result = list(db.sc_lists.find({'item': item_receive},{'_id': 0}))
    # sc_lists라는 키 값으로 구독자 정보 내려주기
    return jsonify({'result':'success', 'sc_lists':result})

@app.route('/order', methods=['POST'])
def saving():
   item_receive = request.form['item_give']
   name_receive = request.form['name_give']
   count_receive = request.form['count_give']
   address_receive = request.form['address_give']
   phone_receive = request.form['phone_give']

   sc_list = {
      'item': item_receive,
      'name': name_receive,
      'count': count_receive,
      'address': address_receive,
      'phone': phone_receive,
   }

   db.sc_lists.insert_one(sc_list)
   return jsonify({'result': 'success'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)