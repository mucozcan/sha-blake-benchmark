import requests
import time
from config import tx_per_block, chain_length, port, tx_amount, tx_endpoint, mining_endpoint, sender_id, recipient_id

for block in range(chain_length):
    for tx in range(tx_per_block):
        data = {'sender': sender_id,
                'recipient': recipient_id,
                'amount':tx_amount}
        res = requests.post(f'http://localhost:{port}{tx_endpoint}',json=data)
        print(res.json())
        time.sleep(0.5)
    res = requests.get(f'http://localhost:{port}{mining_endpoint}')
    print(res.json())
    time.sleep(1)
