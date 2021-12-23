import argparse
from fastapi import FastAPI
from uuid import uuid4
from pydantic import BaseModel
import time

from chain import (BlakeChain, SHAChain)
from merkle_tree import MerkleTree
import config as cfg


if cfg.hash == "blake2b":
    blockchain = BlakeChain()
else:
    blockchain = SHAChain()

merkle_tree = MerkleTree(cfg.hash)

miner_id ="1"

class TX(BaseModel):
    sender = cfg.sender_id
    recipient = cfg.recipient_id
    amount: int

app = FastAPI() 

@app.get('/mine')
def mine(): 
    minig_start = time.time_ns()
    last_block = blockchain.last_block
    last_nonce = last_block['nonce']
    nonce, guess_hash = blockchain.proof_of_work(last_nonce)
    blockchain.new_transaction(
            sender="0",
            recipient=miner_id,
            amount=1,)

    previous_hash = last_block['hash']
    txs = [str(tx) for tx in blockchain.current_transactions]
    merkle_tree.add_leaf(txs, True)
    merkle_tree.make_tree()
    merkle_root = merkle_tree.get_merkle_root()
    block = blockchain.new_block(guess_hash, merkle_root, nonce, previous_hash)
    time_took = time.time_ns() - minig_start
    with open(cfg.results_file, "a") as res_file:
        res_file.write(str(time_took) + "\n")
    response = {
            'message': 'New block added',
            'time took(ns)': time_took,
            'nonce': block['nonce'],
            'index': block['index'],
            'hash': block['hash'],
            'merkle_root': block['merkle_root'],
            'previous_hash': block['previous_hash'],
    }
    merkle_tree.reset_tree()
    return response


@app.post('/tx/new')
def new_transaction(tx: TX):
    index = blockchain.new_transaction(tx.sender, tx.recipient, tx.amount)
    response = {'message':f"Transaction will be added to block {index}",
            'tx': tx}
    return response

@app.get('/chain')
def get_chain():
    response = {
            'chain' : blockchain.chain,
            'length': len(blockchain.chain),
            }

    return response


