from web3 import Web3
from jwt import *
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

	teste10 = deployed_contract.functions.addMatchData("Felpera").call()

	teste11 = deployed_contract.functions.addMatchData("Felpera Muitos").call()



	teste2 = deployed_contract.functions.getTournments().call()

	# print(teste2)

	# teste3 = deployed_contract.functions.getTournmentAddress(web3Instance.to_hex(teste2[1])).call()

	# print(teste3)

	# print(web3Instance.eth)

def main():
	web3_init()

	my_payload = {
	"sub": "1234567890",
	"name": "John Doe",
	"admin": True
	}

	my_secret_key = "42TR4NSC3ND3NC3"

	my_jwt = create_jwt(my_payload, my_secret_key)

	print(my_jwt)

	my_decoded_payload = decode_jwt(my_jwt, my_secret_key)

	print(my_decoded_payload)





if __name__ == '__main__':
	main()