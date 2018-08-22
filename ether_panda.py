import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
import networkx as nx
import math
import scipy

# %%
transactions = pd.read_csv('transactions_nodate')
wallets = transactions['sender'].append(transactions['receiver'])
wallets.nunique() #7880
#check if the returned value is correct
H = nx.read_edgelist("transactions_normalized", nodetype=str, data=(('weight', float),),delimiter=',')
len(H.nodes()) #7880
#=> nunique can be used as count function
(l,b)=transactions.shape # l is the number of lines
#set type of the transactions as float
transactions.amount = transactions.amount.astype(float)
#%%
def snapshotAnalysis(snap): #python does not need a parametertype specification
    assert(snap.ndim == 2) #assure the size of the DataFrame is 2 (actually 3)
    output = pd.Series([]) #save the computed statistical Data in a DataFrame
    (snap_len,b) = snap.shape #alternatively len(snap)

    #number of transactions
    #snap.size returns the number of elements in the dataframe, so not suitable
    output = output.append(pd.Series([snap_len]), ignore_index=True)
    #number of involved wallets
    wallets = snap.iloc[:,0].append(snap.iloc[:,1])
    output = output.append(pd.Series([wallets.nunique()]), ignore_index=True)

    #cumulative amount transferred
    output = output.append(pd.Series([snap.amount.sum()]), ignore_index=True)
    #print(snap.iloc[:,2].sum)

    #average amount per transfer
    output = output.append(pd.Series([snap.amount.sum()/snap_len]), ignore_index=True)
    print(snap.describe())
    return output

for i in range(0,15):
    print(snapshotAnalysis(transactions[10000*i:10000*(i+1)]))


#%%

def userStat(usr, transSet):
    output = pd.DataFrame({'First Transaction' : 0.0, 'Total Transactions' : 0, 'Total Transferred' : 0.0, 'Avg Transferred':0.0, 'Total Received' : 0.0, 'Avg Received': 0.0, 'Balance': 0.0}, index=[1])
    sentTo = transSet[transSet.sender == usr]
    receivedFrom = transSet[transSet.receiver == usr]

    #Todo get familiar with how to extract the date from the block

    #The number of transactions where the user was involved
    count = len(sentTo)
    count += len(receivedFrom)
    output.at[1,'Total Transactions'] = count

    #Sum the total amount transferred to other accounts
    output.at[1,'Total Transferred'] = sentTo.amount.sum()

    #Average amount transferred to other accounts
    if(!sentTo.empty):
        output.at[1,'Avg Transferred'] = sentTo.amount.sum()/len(sentTo)

    #Total amount received by other accounts
    output.at[1,'Total Received'] = receivedFrom.amount.sum()

    #Average amount received
    if(!receivedFrom.empty):
        output.at[1,'Avg Received'] = receivedFrom.amount.sum()/len(receivedFrom)

    #Whats the Balance for the current interval
    output.at[1,'Balance'] = output.at[1,'Total Received'] - output.at[1,'Total Transferred']
    return output

print(userStat('77ec9ad4a7e9418774c29415caaf4ee0da96ef64', transactions))
print(userStat('ethereum', transactions))

#DataFrame(columns=('Transactions','Wallets','Cumulative Amount','Avg amount',''))
#idea: make a table with  balances
