import hashlib
import json
from time import time
from typing import Dict
from config import puzzle

class Chain:
    def __init__(self): 
        self.current_transactions = []
        self.chain = []

        self.new_block(guess_hash="1", previous_hash="1", merkle_root="0", nonce=0) 

    def new_block(self, guess_hash: str, merkle_root: str, nonce: int, previous_hash=None) -> Dict:
        
        header = self.hash({'header': str(previous_hash or self.hash(self.chain[-1])) + str(merkle_root) + str(nonce)})
        block = {
                'index': len(self.chain) + 1,
                'hash': header,
                'guess_hash': guess_hash,
                'nonce': nonce,
                'merkle_root': merkle_root,
                'previous_hash': previous_hash or self.hash(self.chain[-1]['hash']),
        }

        self.current_transactions = []
        self.chain.append(block)

        return block

    def new_transaction(self, sender, recipient, amount) -> int:

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1


    @property 
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block: Dict):
        raise NotImplementedError

    def proof_of_work(self, previous_nonce):
        nonce = 0

        while True: 
            guess_hash = self.valid_proof(previous_nonce, nonce) 
            if guess_hash[:puzzle] == puzzle * "0":
                break
            nonce += 1
            
        return nonce, guess_hash

    @staticmethod
    def valid_proof(previous_nonce, nonce):
        raise NotImplementedError


class BlakeChain(Chain):
    def __init__(self):
        Chain.__init__(self)
    
    @staticmethod
    def hash(block):

        block_string = json.dumps(block).encode('utf-8')
        return hashlib.blake2b(block_string).hexdigest()
    
    @staticmethod
    def valid_proof(previous_nonce, nonce):
        guess = f"{previous_nonce}{nonce}".encode('utf-8')
        return hashlib.blake2b(guess).hexdigest()
         

class SHAChain(Chain):
    def __init__(self):
        Chain.__init__(self)
    
    @staticmethod
    def hash(block):

        block_string = json.dumps(block).encode('utf-8')
        return hashlib.sha256(block_string).hexdigest()
    
    @staticmethod
    def valid_proof(previous_nonce, nonce):
        guess = f"{previous_nonce}{nonce}".encode('utf-8')
        return hashlib.sha256(guess).hexdigest()
