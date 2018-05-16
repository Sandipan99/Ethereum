#create an account-transaction database
#input - account_id and output- list of transactions

import json
import pickle
import pandas as pd

__author__ = 'Sandipan Sikdar'

'''
def insert_trans_account(from_add, to_add, value, time, stat):
    if from_add[0] not in transactions:
        transactions[from_add[0]] = {}
        transactions[from_add[0]][from_add[1]] = {}
        transactions[from_add[0]][from_add[1]][from_add[2]] = {}
        transactions[from_add[0]][from_add[1]][from_add[2]][from_add] = [(stat,time,to_add,value)]
    elif from_add[1] not in transactions[from_add[0]]:
        transactions[from_add[0]][from_add[1]] = {}
        transactions[from_add[0]][from_add[1]][from_add[2]] = {}
        transactions[from_add[0]][from_add[1]][from_add[2]][from_add] = [(stat,time,to_add,value)]
    elif from_add[2] not in transactions[from_add[0]][from_add[1]]:
        transactions[from_add[0]][from_add[1]][from_add[2]] = {}
        transactions[from_add[0]][from_add[1]][from_add[2]][from_add] = [(stat,time,to_add,value)]
    elif from_add not in transactions[from_add[0]][from_add[1]][from_add[2]]:
        transactions[from_add[0]][from_add[1]][from_add[2]][from_add] = [(stat,time,to_add,value)]
    else:
        transactions[from_add[0]][from_add[1]][from_add[2]][from_add].append((stat,time,to_add,value))

def insert_mining_reward(miner, reward, time, stat):
    if miner[0] not in transactions:
        transactions[miner[0]] = {}
        transactions[miner[0]][miner[1]] = {}
        transactions[miner[0]][miner[1]][miner[2]] = {}
        transactions[miner[0]][miner[1]][miner[2]][miner] = [(stat,time,reward)]
    elif miner[1] not in transactions[miner[0]]:
        transactions[miner[0]][miner[1]] = {}
        transactions[miner[0]][miner[1]][miner[2]] = {}
        transactions[miner[0]][miner[1]][miner[2]][miner] = [(stat,time,reward)]
    elif miner[2] not in transactions[miner[0]][miner[1]]:
        transactions[miner[0]][miner[1]][miner[2]] = {}
        transactions[miner[0]][miner[1]][miner[2]][miner] = [(stat,time,reward)]
    elif miner not in transactions[miner[0]][miner[1]][miner[2]]:
        transactions[miner[0]][miner[1]][miner[2]][miner] = [(stat,time,reward)]
    else:
        transactions[miner[0]][miner[1]][miner[2]][miner].append((stat,time,reward))
'''

ft = open("transaction.csv","w")
ft.write("from,to,value,time,block")
ft.write("\n")
ft.close()

def append_transaction(data):
    with open("transaction.csv","a") as ft:
        for obj in data['transactions']:
            ft.write(str(obj['from account'])+","+str(obj['to account'])+","+str(obj['value'])+","+str(data['time'])+","+str(data['number']))
            ft.write("\n")



def insert_mining_reward(data):
    with open("transaction.csv","a") as ft:
        ft.write("ethereum"+","+data['miner'][2:].lower()+","+str(data['reward'])+","+str(data['time'])+","+str(data['number']))
        ft.write("\n")

def extract_info(*argv):
    fname = 'blocks/'
    for arg in argv:
        fname+=str(arg)+'/'
    fname+='blocks'
    try:
        with open(fname) as fs:
            for line in fs:
                data = json.loads(line.strip())
                if data['transaction count'] > 0:
                    append_transaction(data)
                insert_mining_reward(data)
    except:
        print("no such file")

extract_info(0)
for i in range(1,10):
    extract_info(i)
    print ("finished parsing block at: ",i)
    for j in range(10):
        extract_info(i,j)
        print ("finished parsing block at: ",i,j)
        for k in range(10):
            extract_info(i,j,k)
            print ("finished parsing block at: ",i,j,k)
            
