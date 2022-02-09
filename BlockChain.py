from hashlib import sha256
import json
import time

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

class Blockchain: 
    def __init__(self,difficulty ):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()
        self.difficulty=difficulty 
       
    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
    @property
    def last_block(self):
        return self.chain[-1]

    
    def proof_of_work(self, block):
        block.nonce = 0 
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * self.difficulty) and
                block_hash == block.compute_hash())
 
    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True
 
   
    def add_new_transaction(self, transaction):
            self.unconfirmed_transactions.append(transaction)
 
    def mine(self):
        if not self.unconfirmed_transactions:
            return False
 
        last_block = self.last_block
 
        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)
        t1 = time.time()
        proof = self.proof_of_work(new_block)
        t2=time.time()
        ml = int((t2-t1)* 1000)
        print('>>>>>time taken in milliseconds = ', ml)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index
    def check_chain_validity(cls, chain):
        
        result = True
        previous_hash = "0"

        # Iterate through every block
        for block in chain:
            block_hash = block.hash
            # remove the hash field to recompute the hash again
            # using `compute_hash` method.
            delattr(block, "hash")

            if not cls.is_valid_proof(block, block.hash) or \
                    previous_hash != block.previous_hash:
                result = False
                break

            block.hash, previous_hash = block_hash, block_hash

        return result

class peer:
    def __init__(self,basechain):
        self.basechain = basechain
        self.unconfirmed_transactions = basechain.unconfirmed_transactions
        
    def add_transaction(self,unconfirmed_transaction):
        self.basechain.add_new_transaction(unconfirmed_transaction)
       

    def miner(self):
        self.basechain.mine()
    
    def broadcast(self,BlockChain):
        self.basechain = BlockChain
        self.unconfirmed_transactions = BlockChain.unconfirmed_transactions
        

class system:
     def __init__(self,Blockchain):
         self.Blockchain = Blockchain
         self.miners = []

     def choose_longest_chain(self):
        longest_chain = None
        current_len = len(self.Blockchain.chain)
       
        for m in self.miners:

            if len(m.basechain.chain) > current_len and m.basechain.check_chain_validity():
                # Longer valid chain found!
                current_len = len(m.basechain.chain)
                longest_chain = m.basechain
                print('1')
            print('0')
          
        if longest_chain:
            self.Blockchain = longest_chain
            print(json.dumps(longest_chain.__dict__))
            return True

        return False   
     def Broadcast(self):
        self.choose_longest_chain()
        for m in self.miners:
            m.broadcast(self.Blockchain)
          

    
b=Blockchain(int(4))
b.add_new_transaction('alice pay bob 100')
b.add_new_transaction('alice pay bob 200')
s=system(b)
miner1=peer(s.Blockchain)
s.miners.append(miner1)

miner2=peer(s.Blockchain)
s.miners.append(miner2)

s.miners[0].miner()
print('########## miner 1 ##########\t\t')
block_string = json.dumps(s.miners[0].basechain.chain[1].__dict__)
print(block_string)

s.Broadcast()

s.miners[1].miner()

print('########## miner2 ##########\t\t')
block_string = json.dumps(s.miners[1].basechain.chain[1].__dict__)
print(block_string)

s.choose_longest_chain()

    
'''
d = input("add diffculty: ")

chain=Blockchain(int(d))
for i in range (10):
    chain.add_new_transaction('alice pay bob'+ str(i) )
    chain.mine()
    print('##########',i,'##########\t\t')
    block_string = json.dumps(chain.chain[i].__dict__, sort_keys=True)
    print(block_string)
   
'''



