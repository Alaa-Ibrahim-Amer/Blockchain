from hashlib import sha256
import json
from pickle import APPEND
import time
from random import randint

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
        self.difficulty = 4
        self.power = 0
    
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
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        
        

        return True
    
    
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
                current_len = len(m.chain)
                longest_chain = m
               
          
        if longest_chain:
            self.BlockchainMain.chain = longest_chain.chain
            return True

        return False   
     
     def Broadcast(self):
        self.choose_longest_chain()
        for m in self.miners:
            m.chain = self.BlockchainMain.chain +[]
     
     def add_miner(self):
        self.miners.append(Blockchain())
        
     def minebyminer(self):
            i=0
            j=0
            
            for m in self.miners:
                    if  m.power != 11 :
                        m.power = randint(0, 10)
                    if m.power >= i:
                        index=j
                        i=m.power
                    j=j+1
                    
            self.miners[index].add_new_transaction(self.BlockchainMain.unconfirmed_transactions)       
            b = self.miners[index].mine()
            if b == True:
              self.BlockchainMain.unconfirmed_transactions =[]  

            return index
    

'''
# attacker speed scenario
b=Blockchain()
b.add_new_transaction('transaction 0')
s=system(b)
s.add_miner() #miner [0]
s.add_miner() #attacker miner [1]

s.minebyminer()
s.Broadcast()

attacker=Blockchain()
attacker.chain = s.miners[0].chain + []
attacker.power = 10
attacker.add_new_transaction ('attacker transaction') #duoble spending
attacker.mine()

s.miners[0].chain = []
s.miners[0].chain = attacker.chain + [] #attack here
s.miners[0].power = attacker.power
#s.Broadcast()

i=1
for i in range (5) :
    s.BlockchainMain.add_new_transaction('transaction'+ str(i) )
    index = s.minebyminer()
    print('block',index,' mine the block')


time_attack = []
for x in s.miners[0].chain:
    time_attack.append( x.timestamp)
y = 0
total_time = 0
for y in range (len(time_attack)-1):
    total_time = total_time + time_attack[y+1] - time_attack[y]
    
total_time = time.time() - total_time
print ('time taken by attacker', time.localtime(total_time).tm_sec)
print ('speed of attacker', time.localtime(total_time).tm_sec /len(s.miners[0].chain) )

legit_time = []
for x in s.miners[1].chain:
    legit_time.append( x.timestamp)
yy = 0
total_time_ = 0
for yy in range (len(legit_time)-1):
    total_time_ = total_time_ + legit_time[yy+1] - legit_time[yy]
    
total_time_ = time.time() - total_time_

print ('time taken by miners', time.localtime(total_time_).tm_sec)
print ('speed of miners', time.localtime(total_time_).tm_sec /len(s.miners[1].chain) )

s.Broadcast()
for m in s.BlockchainMain.chain:
    print('###########chain after attack#########\t\t')
    block_string = json.dumps(m.__dict__)
    print(block_string)
'''


# attacker scenario
b=Blockchain()
b.add_new_transaction('transaction before attack')
s=system(b)
s.add_miner() #miner [0]
s.add_miner() #miner [1]
s.add_miner() #attacker miner [2]

s.minebyminer()
s.Broadcast()

attacker=Blockchain()
attacker.chain = s.miners[2].chain + []
attacker.power = 11
attacker.add_new_transaction ('attacker transaction') #duble spindding
attacker.mine()

for m in s.BlockchainMain.chain:
    print('###########chain before attack#########\t\t')
    block_string = json.dumps(m.__dict__)
    print(block_string)

s.BlockchainMain.add_new_transaction('transaction while attackeing 1 ') 
s.minebyminer()
s.BlockchainMain.add_new_transaction('transaction while attacking 2 ') 
s.minebyminer()


s.Broadcast() #broadcast2

for m in s.BlockchainMain.chain:
    print('##########chains before the attacker become the longest chain##########\t\t')
    block_string = json.dumps(m.__dict__)
    print(block_string)



s.miners[2].chain = []
s.miners[2].chain = attacker.chain + [] #attack here
s.miners[2].power = attacker.power

s.BlockchainMain.add_new_transaction('transaction after attacking 1') 
s.minebyminer()
s.BlockchainMain.add_new_transaction('transaction after attacking 2') 
s.minebyminer()


s.Broadcast()

for m in s.BlockchainMain.chain:
    print('###########chain after attack#########\t\t')
    block_string = json.dumps(m.__dict__)
    print(block_string)






    
'''
#difficulty scenario 
d = input("add diffculty: ")
chain=Blockchain()
chain.difficulty = int (d)
for i in range (5):
    chain.add_new_transaction('alice pay bob'+ str(i) )
    t1=time.time()
    chain.mine()
    t2=time.time()
    timetaken =int ( t2-t1 ) * 1000
    print('>>>>>time taken by block',i,' in milliseconds = ', timetaken)
'''



'''
#dynamic difficulty scenario 
def control_hardness (Blockchain,timeDiff):
    N = Blockchain.difficulty
    M = Blockchain.difficulty
    if (1000 > timeDiff):
        N = N + 1
    if (1000 <= timeDiff and N - 1 > 0 ):
        N = N - 1
    Blockchain.difficulty = N
    print('difficulty changes from: ',M,'to: ',N)
   

d = input("starting diffculty: ")
chain=Blockchain()
chain.difficulty = int (d)
timetaken = 0
for i in range (10):
    chain.add_new_transaction('alice pay bob'+ str(i) )
    control_hardness (chain,timetaken)
    t1=time.time()
    chain.mine()
    t2=time.time()
   
    timetaken =int ( t2-t1 ) * 1000
    print('>>>>>time taken by block',i,' in milliseconds = ', timetaken)
   
'''
   



