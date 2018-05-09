import json

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
	for key in data:
		print(key+": "+str(data[key]))

#def retrieve_account_transaction(account,timestamp):


def getTransactions(block_num):
	data = 

if __name__=="__main__":
	retrieveBlock(409912)					