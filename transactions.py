#create an account-transaction database
#input - account_id and output- list of transactions

import json

__author__ = 'Sandipan Sikdar'

transactions = {}

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

def append_transaction(data):
    for obj in data['transactions']:
        from_add = obj['from account']
        to_add = obj['to account']
        value = obj['value']
        time = data['time']
        insert_trans_account(from_add, to_add, value, time, 1)
        insert_trans_account(to_add, from_add, value, time, 0)

def extract_info(*argv):
    fname = ''
    for arg in argv:
        fname+=str(i)+'/'
    fname+='blocks'
    try:
        with open(fname) as fs:
            for line in fs:
                data = json.loads(line.strip())
                if data['transaction count'] > 0:
                    append_transaction(data)
                insert_mining_reward(data['miner'][2:].lower(), data['reward'], time, 2)
    except:
        print("no such file")

for i in range(10):
    extract_info(i)
    for j in range(10):
        extract_info(i,j)
        for k in range(10):
            extract_info(i,j,k)
