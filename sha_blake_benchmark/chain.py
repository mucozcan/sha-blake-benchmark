import hashlib
import json
from time import time
from typing import Dict
from config import nonce
from merkle_tree import BlakeMerkleTree, SHAMerkleTree

class Chain:
    def __init__(self): 
        self.current_transactions = []
        self.chain = []

        self.new_block(proof=100, previous_hash="1", merkle_root="0", guess_hash="1") # genesis block

    def new_block(self, proof: int, merkle_root: str, previous_hash=None, guess_hash=None) -> Dict:
        
        block = {
                'index': len(self.chain) + 1,
                'timestamp': time(),
                'nonce': guess_hash or self.hash(self.chain[-1]),
                'merkle_root': merkle_root,
                'proof': proof,
                'previous_hash': previous_hash or self.hash(self.chain[-1]),
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

    def proof_of_work(self, previous_proof):
        proof = 0

        while True: 
            guess_hash = self.valid_proof(previous_proof, proof) 
            if guess_hash[:nonce] == nonce * "0":
                print(guess_hash)
                break
            proof += 1
            
        return proof, guess_hash

    @staticmethod
    def valid_proof(previous_proof, proof):
        raise NotImplementedError


class BlakeChain(Chain):
    def __init__(self):
        Chain.__init__(self)
    
    @staticmethod
    def hash(block):

        block_string = json.dumps(block).encode('utf-8')
        return hashlib.blake2b(block_string).hexdigest()
    
    @staticmethod
    def valid_proof(previous_proof, proof):
        guess = f"{previous_proof}{proof}".encode('utf-8')
        return hashlib.blake2b(guess).hexdigest()
         

class SHAChain(Chain):
    def __init__(self):
        Chain.__init__(self)
    
    @staticmethod
    def hash(block):

        block_string = json.dumps(block).encode('utf-8')
        return hashlib.sha256(block_string).hexdigest()
    
    @staticmethod
    def valid_proof(previous_proof, proof):
        guess = f"{previous_proof}{proof}".encode('utf-8')
        return hashlib.sha256(guess).hexdigest()
