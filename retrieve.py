# Implements several functions for retrieving information from blocks
# Function names are self-explanatory

import json
import pickle
import pandas as pd

__author__ = 'Sandipan Sikdar'

def retrieveBlock(block_num):
	b_str = str(block_num)
	path = 'blocks/'
	## finding the file path for the block.....3 levels of hashing
	if len(b_str)>=3:
		path += b_str[0]+"/"+b_str[1]+"/"+b_str[2]+"/"
	elif len(b_str)==2:
		path += b_str[0]+"/"+b_str[1]+"/"
	else:
		path += b_str[0]+"/"

	file_name = path+"blocks"

	with open(file_name) as fs:
		for line in fs:
			data = json.loads(line.strip())
			if data['number'] == block_num:
				return data
	return None


def displayBlock(block_num):
	data = retrieveBlock(block_num)
	if data==None:
		print("block not found")
	else:
		for key in data:
			print(key+": "+str(data[key]))

#def retrieve_account_transaction(account,timestamp):


def getTransactions(block_num):
	data = retrieveBlock(block_num)
	if data==None:
		return None
	elif data['transaction count'] == 0:
		return None
	else:
		return data['transactions']

def displayTransactions(block_num):
	trans = getTransactions(block_num)
	if trans==None:
		print("No transactions found for this block")
	else:
		for i in range(len(trans)):
			for key in trans[i]:
				print(key+": "+str(trans[i][key]))

def retrieveTransactionAccount(a): #returns a data frame
	trans = pd.read_csv("transaction.csv")
	df1 = trans['from' == a]
	df2 = trans['to' == a]
	return trans[df1 | df2]

if __name__=="__main__":
	#print(retrieveTransactionAccount('0000000000000000000000000000000000000000'))
	print(displayBlock(0))
