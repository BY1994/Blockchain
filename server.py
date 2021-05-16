from flask import Flask, request, jsonify
import json
from uuid import uuid4

# Our blockchain.py API
from blockchain import Blockchain

app = Flask(__name__)
# Universial Unique Identifier
# 노드 식별을 하기 위해 uuid 함수를 사용!
node_identifier = str(uuid4()).replace('-','')

# 아까 짜놓은 블록체인 객체를 선언
blockchain = Blockchain()

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain' : blockchain.chain, # 블록체인을 출력
        'length' : len(blockchain.chain), # 블록체인 길이 출력
    }

    # json 형태로 리턴 (200 은 웹 사이트 에러가 없을 때 뜨는 숫자)
    return jsonify(response), 200

# post는 url에 데이터를 붙여서 보내는 get과 달리 숨겨서 보내는 방식
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json() # json 형태를 받아서 저장

    required = ['sender', 'recipient', 'amount'] # 해당 데이터가 존재해야함
    # 데이터가 없으면 에러를 띄움
    if not all(k in values for k in required):
        return 'missing values', 400

    # Create a new Transaction
    # 새 트랜잭션 만들고 삽입
    index = blockchain.new_transaction(values['sender'],values['recipient'],values['amount'])
    response = {'message' : 'Transaction will be added to Block {%s}' % index}

    return jsonify(response), 201

# 채굴이 되게 할 것
# coinbase transaction: 채굴할 때마다 1 코인씩 준다
@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']

    proof = blockchain.pow(last_proof)

    blockchain.new_transaction(
        sender='0', # 채굴시 생성되는 transaction (0 = 운영자)
        recipient=node_identifier, # 지갑 주소처럼 사용
        amount=1 # coinbase transaction
    )
    # Forge the new Block by adding it to the chain
    # 전 블록에 대한 hash를 떠놓고
    previous_hash = blockchain.hash(last_block)
    # 검증하는 걸 넣어서 블록을 새로 생성
    block = blockchain.new_block(proof, previous_hash)

    # block 이 제대로 mine 되었다는 정보를 json 형태로 띄워줌
    response = {
        'message' : 'new block found',
        'index' : block['index'],
        'transactions' : block['transactions'],
        'proof' : block['proof'],
        'previous_hash' : block['previous_hash']
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)