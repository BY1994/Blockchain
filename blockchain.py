import hashlib # hash 함수용 sha256 사용할 라이브러리
import json
from time import time
# from urlparse import urlparse
from urllib.parse import urlparse

class Blockchain(object):
    def __init__(self):
        self.chain = [] # chain에 여러 block들 들어옴
        self.current_transaction = [] # 임시 transaction 넣어줌

        # genesis block 생성
        self.new_block(previous_hash=1, proof=100)
    
    def new_block(self, proof, previous_hash=None):
        # Creates a new Block and adds it to the chain
        block = {
            'index' : len(self.chain)+1,
            'timestamp' : time(), # timestamp from 1970
            'transactions' : self.current_transaction,
            'proof' : proof,
            'previous_hash' : previous_hash or self.hash(self.chain[-1]);
        }
        self.current_transaction = []
        self.chain.append(block)
        return block

    def new_transaction(self):
        # Adds a new transaction to the list of transaction
        self.current_transaction.append(
            {
                'sender' : sender, # 송신자
                'recipient' : recipient, # 수신자
                'amount' : amount # 금액
            }
        )
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        # Hashes a Block
        block_string = json.dumps(block, sort_keys=True).encode()

        # hash 라이브러리로 sha256 사용
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]

    def pow(self, last_proof):
        proof = 0
        # valid proof 함수를 통해 맞을 때까지 반복적으로 검증
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        # 전 proof와 구할 proof 문자열 연결
        guess = str(last_proof + proof).encode()
        # 이 hash 값 저장
        guess_hash = hashlib.sha256(guess).hexdigest()
        # 앞 4자리가 0000 이면 True
        return guess_hash[:4] == "0000" # nonce
