from web3 import Web3
from jwt import *
import json

# HardCode do address smart contract

TNM_ADDRESS = '4def4fc111fd970a96b17ebea40b6e8a'

def get_contract():
	with open('/home/femoyo/Documents/transcendence/blockchain/hardhat/artifacts/contracts/Tournaments.sol/Tournament.json') as f:
		contract = json.load(f)
	return contract

def web3_init():
	contract = get_contract()

	web3Instance = Web3(Web3.HTTPProvider('http://localhost:8545/'))


	Tournament = web3Instance.eth.contract(abi=contract['abi'], bytecode=contract['bytecode'])

	account = web3Instance.eth.accounts[0]

	tx_hash = Tournament.constructor().transact({'from': account})

	tx_receipt = web3Instance.eth.wait_for_transaction_receipt(tx_hash)

	try:
		account2 = web3Instance.eth.accounts[1]
		teste11 = deployed_contract.functions.addMatch("Hello Not Owner").transact({'from': account2})
	except Exception as e:
		print(e)

	deployed_contract = web3Instance.eth.contract(address=tx_receipt.contractAddress, abi=contract['abi'])
	
	str1 = 'Hello World'
	webText1 = web3Instance.to_hex(text=str1)
	print(type(webText1), "1")
	add1 = deployed_contract.functions.addMatch(webText1).transact({'from': account})
	web3Instance.eth.wait_for_transaction_receipt(tx_hash)

	str2 = 'Hello Blockchain'
	webText2 = web3Instance.to_hex(text=str2)
	print(type(webText2), "2")
	add2 = deployed_contract.functions.addMatch(webText2).transact({'from': account})
	web3Instance.eth.wait_for_transaction_receipt(tx_hash)


	str3 = 'Hello Darkness'
	webText3 = web3Instance.to_hex(text=str3)
	print(type(str3), "3")
	add3 = deployed_contract.functions.addMatch(webText3).transact({'from': account})
	web3Instance.eth.wait_for_transaction_receipt(tx_hash)

	for i in range(0, 3):
		print(type(web3Instance.to_int(i)))
		teste2 = deployed_contract.functions.getMatchIndex(web3Instance.to_int(i)).call()
		print(web3Instance.to_text(teste2))


def main():
	web3_init()

	my_payload = {
	"sub": "1234567890",
	"name": "John Doe",
	"admin": True
	}

	my_secret_key = "42TR4NSC3ND3NC3"

	my_jwt = create_jwt(my_payload, my_secret_key)

	# print(my_jwt)

	my_decoded_payload = decode_jwt(my_jwt, my_secret_key)

	# print(my_decoded_payload)





if __name__ == '__main__':
	main()