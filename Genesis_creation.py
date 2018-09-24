import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import math
import scipy
from web3 import Web3, IPCProvider
import time
import datetime
import csv
from multiprocessing import Process, Lock, Queue,Pool, Manager
#%%
#Note: in the all transactions file, the names of the columns are in low caps
transactions = pd.read_csv('all_transactions.csv')
#transactions = pd.read_csv('transaction_till_100000.csv', low_memory=False)
print('Read the transactions into panda frame')
wallets = set(transactions['from'].append(transactions['to']))

def genesis_comp(accList):
    for acc in accList:
        nextGen = transactions[transactions.From == acc]
        for row in nextGen.itertuples():
            Genesis[row[2]] = min(Genesis[row[1]] + 1,abs(Genesis[row[2]]))

    # for acc in wallE:
    #     # for trAc in transactions.itertuples():
    #     # max(Genesis.items(), key=lambda x:x[1])[1]
    #     #     if trAc[1] == acc:
    #     #         Genesis[acc[2]] = Genesis[acc]+1

if __name__ == '__main__':
    manager= Manager()
    num = 6 #the number of processes used
    lvl = 0 #the current level of wallets considered
    Genesis = manager.dict()

    for trAc in transactions.itertuples():
        Genesis[trAc[2]] = -2000000
        if trAc[1] == 'ethereum':
            Genesis[trAc[2]] = 1
    print("Initialization completed ")
    #Iterate until no wallets are left to check
    wallE = [acc for (acc,score) in Genesis.items() if score > lvl]
    while lvl < 10:
        # Compute the set of wallets for the next iteration
        print(len(wallE))
        wallESeq = [wallE[i::num] for i in range(num)] #Split the accounts into working chunks
        for n in range(num):
            p = Process(target=genesis_comp, args=(wallESeq[n],))
            p.start()
            p.join() #join is necessary, otherwise off-sync with rest
        lvl= lvl+1
        print(lvl)
        wallE = [acc for (acc,score) in Genesis.items() if score > lvl]


#Print the genesis dict to a csv file
with open('genesis.csv', 'w',newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|')
    spamwriter.writerow(['acc'] + ['score'])
    for (acc, score) in Genesis.items():
        if score > 1:
            spamwriter.writerow([acc] + [score])
print('Wrote genesis to file')


    #i=0
    # wallE = [row[1] for row in transactions.itertuples() if row[0]< 10]
    # print('Size of wallets: %i and the level is %i ' %(len(wallE), 0))
    # for acc in wallE:
    #     wallQ.put(acc) #Enqueue all current wallets to the working Queue
    # #for i in range (0,10):

    #
