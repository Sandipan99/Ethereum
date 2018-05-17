Here I have jotted down different aspects the ethereum block chain ---


1. Opening an account and joining the network ---

	1.1. The easiest way is to download a ethereum wallet from https://www.ethereum.org/ and install it. Then open the wallet. You will have the option to connect to the main network (default) or a smaller test network. Once connected the application will download the whole blockchain which for the main network is close to 68GB  as of 9th April 2018. The chain data is downloaded to the location /Users/sandipansikdar/Library/ethereum/geth/chaindata (for Mac).

	1.2. Another way around is through packages available in python (pyethereum), C++ (cpp-ethereum), go (geth, app mentioned in 1.1 is a go implementation) and others. Installation procedures are described in the respective developer pages. I had initially installed pyethereum but failed to connect to the network and hence had to shift to geth.


2. Exploring the chain ---

	2.1. All information (live) related to the blockchain are maintained in the several websites. Most popular of them being etherscan.io

	2.2. One can also explore the blockchain from the downloaded chain data through --

		2.2.1. JSON RPC: I was not able to connect with MAC.

		2.2.2. geth-ipc: For this one needs to connect a geth client to the network which can be done by opening a terminal and executing the command "geth". This will create a file geth.ipc at /Users/sandipansikdar/Library/ethereum/. Now open a terminal and execute "geth attach ipc://Users/sandipansikdar/Library/ethereum/geth.ipc". Now on the console one can execute functions specified in https://github.com/ethereum/wiki/wiki/JavaScript-API#web3eth to mine information from the chain data.

		2.2.3. A new library in python has been published Web3.py which provides a python interface to the api discussed in 2.2.2
		http://web3py.readthedocs.io/en/stable/quickstart.html

	2.3. Since extracting data requires geth client to be online and is slow, it is not viable to use it for large scale experiments.

		2.3.1. The script "build_data_base.py" reads the chain data and creates a json database consisting of all the block in formation. The data is stored following a 3-level hashing and retrieval is quicker. Once the database is constructed, the chain data is no longer required. Neither a geth client.

		2.3.2. "retrieve.py" defines several functions (the names are self explanatory) for retrieving informations related to a particular block. I plan to enrich it with more functions.

		2.3.3. "transactions.py" creates a csv file which lists all the transactions across all the blocks including mining rewards.
		2.3.4. Uncle rewards are stored separately using the getUncleRewards() function in build_data_base.py
