from hashlib import sha256
import json
from sqlite3 import Timestamp
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
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()
     #   self.difficulty=self.calculate_difficulty() 
        self.difficulty = 4
    
    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
    @property
    def last_block(self):
        return self.chain[-1]

    ''''
    def calculate_difficulty(self):
        difficulty = 0
        t1 = time.time()
        for i in range (10):
            self.chain.add_new_transaction('alice pay bob 100')
            self.chain.mine()

        t2=time.time()
        ml = int((t2-t1)* 1000)
        print('>>>>>time taken in milliseconds = ', ml)
        print('##########',i,'##########\t\t')
        block_string = json.dumps(self.chain.chain[i].__dict__, sort_keys=True)
        print(block_string)

        return difficulty

    '''


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
        #t1 = time.time()
        proof = self.proof_of_work(new_block)
        #t2=time.time()
        #ml = int((t2-t1)* 1000)
        #print('>>>>>time taken in milliseconds = ', ml)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        
        

        return True
    '''
    def check_chain_validity(self, chain):
        
        result = True
        previous_hash = "0"
        # Iterate through every block
        for block in chain:
            block_hash = block.hash
            # remove the hash field to recompute the hash again
            # using `compute_hash` method.
            delattr(block, "hash")

            if not self.is_valid_proof(block, block.hash) or \
                    previous_hash != block.previous_hash:
                result = False
                break

            block.hash, previous_hash = block_hash, block_hash
        print('55',result)
        return result
    '''
    def copy_chain(self,Blockchain):
        self.chain = Blockchain.chain
        self.difficulty = Blockchain.difficulty
        self.unconfirmed_transactions = Blockchain.unconfirmed_transactions


class system:
     def __init__(self,BlockchainMain):
         self.BlockchainMain = BlockchainMain
         self.miners = [] # list of Blockchain

     
     def choose_longest_chain(self):
        longest_chain = None
        current_len = len(self.BlockchainMain.chain)
       
        for m in self.miners:

            if len(m.chain) > current_len :
                # Longer valid chain found!
                current_len = len(m.chain)
                longest_chain = m
               
          
        if longest_chain:
            self.BlockchainMain = longest_chain
            print('last block in longest chain',json.dumps(longest_chain.chain[-1].__dict__))
            return True

        return False   
     
     def Broadcast(self):
        self.choose_longest_chain()
        for m in self.miners:
            m.chain = self.BlockchainMain.chain
     
     def add_miner(self):
        self.miners.append(Blockchain())
        #self.miners[-1].add_new_transaction(self.BlockchainMain.unconfirmed_transactions)
        #s.miners[-1].copy_chain(self.BlockchainMain)
     def minebyminer(self,i):
        self.miners[i].add_new_transaction(self.BlockchainMain.unconfirmed_transactions)       
        b = self.miners[i].mine()
        if b == True:
            self.BlockchainMain.unconfirmed_transactions =[]        



b=Blockchain()
b.add_new_transaction('alice pay bob 100')

s=system(b)
s.add_miner()
s.minebyminer(0)
print('########## miner 1 ##########\t\t')
block_string = json.dumps(s.miners[0].chain[-1].__dict__)
print(block_string)

s.BlockchainMain.add_new_transaction('alice pay bob 200')
s.add_miner()
s.minebyminer(0)

print('########## miner 0 ##########\t\t')
block_string = json.dumps(s.miners[1].chain[-1].__dict__)
print(block_string)
print('########## base len ##########\t\t')
s.Broadcast()
print('########## miner 0 ##########\t\t')
block_string = json.dumps(s.miners[1].chain[1].__dict__)
print(block_string)


print(len(b.chain))


#s.Broadcast()

#s.miners[1].miner()

#print('########## miner2 ##########\t\t')
#block_string = json.dumps(s.miners[1].basechain.chain[1].__dict__)
#print(block_string)



#s.choose_longest_chain()

    








'''
def control_hardness (Blockchain):
    t1 = Blockchain.chain[0].timestamp
    t2 = time.time()
    timeDiff =  int((t2 - t1) * 1000)
    
    while(Blockchain.difficulty < 4):
        print('>>>>>time taken in milliseconds = ', timeDiff)
        if(timeDiff >= 0):
            Blockchain.difficulty =  Blockchain.difficulty + 1
        if(timeDiff >= 1200 and  Blockchain.difficulty > 1):
            Blockchain.difficulty =  Blockchain.difficulty - 1
        print ( Blockchain.difficulty)
    

chain=Blockchain()

chain.add_new_transaction('alice pay bob')
chain.mine()
print('####################\t\t')
block_string = json.dumps(chain.chain[-1].__dict__, sort_keys=True)
print(block_string)
control_hardness(chain)
'''




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



