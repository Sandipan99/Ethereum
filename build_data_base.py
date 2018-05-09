# this code uses web3.py package to create a block databases
# Block: This is a json file which stores all the block information upto block number 5420000 with 3 levels of hashing..
# uses multiprocessing library to parallelize...

__author__ = 'Sandipan Sikdar'

from web3 import Web3, IPCProvider
import json
import pickle
from binascii import hexlify
from multiprocessing import Process
import time

#no_transaction = []

def convert_string(hex_bytes):
	return str(hexlify(hex_bytes))[2:-1]

w3 = Web3(IPCProvider('/Users/sandipansikdar/Library/ethereum/geth.ipc'))

def getBlockInformation(start_block):

	while start_block>0:
		final_block = (start_block + 1)*10000 - 1
		end_block = start_block*10000
		#final_block = 5391108
		#end_block = 5390000
		block_iterator = final_block

		block_time = {}
		flag = 0
		while block_iterator >= end_block:
			b_str = str(block_iterator)
			t_count = w3.eth.getBlockTransactionCount(block_iterator)
			transactions = []
			path = 'blocks/'
			## finding the file path for the block.....3 levels of hashing
			if len(b_str)>=3:
				path += b_str[0]+"/"+b_str[1]+"/"+b_str[2]+"/"
			elif len(b_str)==2:
				path += b_str[0]+"/"+b_str[1]+"/"
			else:
				path += b_str[0]+"/"

			## extracting information from the block....
			block = w3.eth.getBlock(block_iterator)
			mining_reward = 0

			if t_count>0:
				for i in range(t_count):
					t_hash = block.transactions[i]
					trans = w3.eth.getTransactionFromBlock(block_iterator,i)
					trans_rec = w3.eth.getTransactionReceipt(t_hash)
					mining_reward += trans_rec.gasUsed*trans.gasPrice


					# find hashed numbers of the to and from accounts....
					try:
						transactions.append({'block Number':trans.blockNumber, 'from account':trans['from'][2:].lower(), 'to account':trans.to[2:].lower(), 'value':trans.value, 'gas':trans.gas, 'gas price':trans.gasPrice, 'gas used':trans_rec.gasUsed, 't_index':i})
					except:
						continue


			if block_iterator>4369999:
				mining_reward+=3000000000000000000
			else:
				mining_reward+=5000000000000000000

			with open(path+"blocks","a") as ft:
				json.dump({'extra data':convert_string(block.extraData), 'gas limit':block.gasLimit, 'hash':convert_string(block.hash), 'number':block.number, 'time':block.timestamp, 'miner':block.miner, 'gas used':block.gasUsed, 'transaction count':t_count, 'transactions':transactions, 'reward':mining_reward},ft)
				ft.write("\n")


			print ("finished processing block: ",block_iterator)
			block_iterator-=1
		start_block-=1
		#time.sleep(120)


if __name__=="__main__":
	#getBlockInformation(1)
	jobs = []
	args = 542
	for i in range(4):
		jobs.append(Process(target=getBlockInformation, args=(args,)))
		args-=1

	for j in jobs:
		j.start()
	for j in jobs:
		j.join()
