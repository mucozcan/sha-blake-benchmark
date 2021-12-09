from uuid import uuid4

hash = "sha256"

sender_id = str(uuid4()).replace('-', '')
recipient_id = str(uuid4()).replace('-', '')

puzzle = 6
chain_length = 10
tx_per_block=6
tx_amount=10

port = 4544
tx_endpoint = "/tx/new"
mining_endpoint = "/mine"
results_file = "./results/sha256/sha256_round9.txt"

"""
always 10 blocks

round1:
    puzzle=2:
        tx per block=2

round2:
    puzzle=2:
        tx per block=4

round3:
    puzzle=2:
        tx per block=6

round4:
    puzzle=4:
        tx per block=2

round5:
    puzzle=4:
        tx per block=4

round6:
    puzzle=4:
        tx per block=6
        
round7:
    puzzle=6:
        tx per block=2

round8:
    puzzle=6:
        tx per block=4

round9:
    puzzle=6:
        tx per block=6    
"""
