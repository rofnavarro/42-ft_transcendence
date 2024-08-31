from web3 import Web3
import json

# HardCode do address smart contract

TNM_ADDRESS = '4def4fc111fd970a96b17ebea40b6e8a'

def get_contract():
	with open('/home/femoyo/Documents/transcendence/blockchain/hardhat/artifacts/contracts/Tournments.sol/Tournment.json') as f:
		contract = json.load(f)
	return contract

def web3_init():
	contract = get_contract()

	web3Instance = Web3(Web3.HTTPProvider('http://localhost:8545/'))


	Tournment = web3Instance.eth.contract(abi=contract['abi'], bytecode=contract['bytecode'])

	account = web3Instance.eth.accounts[0]

	tx_hash = Tournment.constructor().transact({'from': account})

	tx_receipt = web3Instance.eth.wait_for_transaction_receipt(tx_hash)

	deployed_contract = web3Instance.eth.contract(address=tx_receipt.contractAddress, abi=contract['abi'])

	teste1 = deployed_contract.functions.addMatchData("Hello World").call()

	teste1 = deployed_contract.functions.addMatchData("Felpera").call()

	teste1 = deployed_contract.functions.addMatchData("Felpera Muitos").call()



	teste2 = deployed_contract.functions.getTournments().call()

	print(teste2)

	# teste3 = deployed_contract.functions.getTournmentAddress(web3Instance.to_hex(teste2[1])).call()

	# print(teste3)

	# print(web3Instance.eth)

def main():
	web3_init()



if __name__ == '__main__':
	main()