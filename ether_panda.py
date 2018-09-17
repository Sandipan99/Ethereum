import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
import networkx as nx
import math
import scipy
from web3 import Web3, IPCProvider
import time
import datetime


#Todo: The first transaction timestamp does not seem correct

# %%
transactions = pd.read_csv('transactions_nodate')
wallets = transactions['From'].append(transactions['To'])
nWallets = wallets.nunique() #7880

(l,b)=transactions.shape # l is the number of lines
#set type of the transactions as float
transactions.Value = transactions.Value.astype(float)

#%%

def dateToUnixTime(date):
   return time.mktime(datetime.datetime.strptime(date, “%Y-%m-%d”).timetuple())

#%%
def snapshotAnalysis(snap):
    output = pd.Series([]) #save the computed statistical Data in a DataFrame
    (snap_len,b) = snap.shape #alternatively len(snap)
    #assert(b = 3)

    #number of transactions
    #snap.size returns the number of elements in the dataframe, so not suitable
    output = output.append(pd.Series([snap_len]), ignore_index=True)
    #number of involved wallets
    wallets = snap.iloc[:,0].append(snap.iloc[:,1])
    output = output.append(pd.Series([wallets.nunique()]), ignore_index=True)

    #cumulative amount transferred
    output = output.append(pd.Series([snap.Value.sum()]), ignore_index=True)
    #print(snap.iloc[:,2].sum)

    #average amount per transfer
    output = output.append(pd.Series([snap.Value.sum()/snap_len]), ignore_index=True)
    print(snap.describe())
    return output
#%%

def userStat(usr, transSet):
    output = pd.DataFrame({'First Transaction' : '', 'Total Transactions' : 0, 'Total Transferred' : 0.0, 'Max Transferred':0.0, 'Avg Transferred':0.0, 'Most Frequent': '', 'Total Received' : 0.0, 'Avg Received': 0.0, 'Balance': 0.0}, index=[1])
    sentTo = transSet[transSet.From == usr]
    receivedFrom = transSet[transSet.To == usr]

    #Todo get familiar with how to extract the date from the block
    allUsr = sentTo.append(receivedFrom,ignore_index = True)
    output.at[1,'First Transaction'] = usr
    # allUsr.sort_values(by='Time').at[0,'Time']

    #The number of transactions where the user was involved
    count = len(sentTo)
    count += len(receivedFrom)
    output.at[1,'Total Transactions'] = count

    #Sum the total amount transferred to other accounts
    output.at[1,'Total Transferred'] = sentTo.Value.sum()

    #Maximum amount transferred
    if sentTo.empty:
        output.at[1,'Max Transferred'] =  0.0
    else:
        output.at[1,'Max Transferred'] = max(sentTo.Value)


    #Average amount transferred to other accounts
    if not sentTo.empty:
        output.at[1,'Avg Transferred'] = sentTo.Value.sum()/len(sentTo)

    #To whom did the Account transfer most often
    numTrans = [] #use a list that contains lists of size two
    uniq = sentTo.To.tolist()
    for usr in sentTo.To.unique():
        numTrans.append((usr,uniq.count(usr)))
    numTrans = sorted(numTrans, key = lambda x: x[1],reverse = True)
    if numTrans:
        output.at[1,'Most Frequent'] = numTrans[0]

    #Total amount received by other accounts
    output.at[1,'Total Received'] = receivedFrom.Value.sum()

    #Average amount received
    if not receivedFrom.empty:
        output.at[1,'Avg Received'] = receivedFrom.Value.sum()/len(receivedFrom)

    #Whats the Balance for the current interval
    output.at[1,'Balance'] = output.at[1,'Total Received'] - output.at[1,'Total Transferred']



    return output


#%%
#Make a list of all userStats for a certain period of time
timeSet = transactions
wallets = set(transactions['From'].append(transactions['To']))-set('ethereum')
stats = pd.DataFrame({'First Transaction' : '', 'Total Transactions' : 0, 'Total Transferred' : 0.0, 'Max Transferred':0.0, 'Avg Transferred':0.0, 'Most Frequent': '', 'Total Received' : 0.0, 'Avg Received': 0.0, 'Balance': 0.0}, index=[1])
for usr in wallets:
    stats = stats.append(userStat(usr,timeSet), ignore_index = True)
print(stats)
stats.describe()
stats.sort_values(by='Total Received')
#%%
