from .models import Tournament
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import QuerySet
from django.conf import settings
from users.models import CustomUser
import datetime
import json

#Imports the web3 module
from web3 import Web3
import json


def get_contract():
	with open('/home/femoyo/Documents/transcendence/blockchain/hardhat/artifacts/contracts/Tournaments.sol/Tournament.json') as f:
		contract = json.load(f)
	return contract

#TODO: achar uma forma de executar apenas 1x o web3_init
def web3_init():
	contract = get_contract()
	web3Instance = Web3(Web3.HTTPProvider('http://localhost:8545/'))
	Tournament = web3Instance.eth.contract(abi=contract['abi'], bytecode=contract['bytecode'])
	account = web3Instance.eth.accounts[0]
	try:
		settings.TX_HASH = (Tournament.constructor().transact({'from': account}))
		settings.TX_RECEIPT.append(web3Instance.eth.wait_for_transaction_receipt(settings.TX_HASH))
	except Exception as e:
		pass
	return (web3Instance)

def deploy_contract(web3):
	contract = get_contract()
	deployed_contract = web3.eth.contract(address=settings.TX_RECEIPT[0].contractAddress, abi=contract['abi'])
	return (deployed_contract)

#---------------------------------------------


def set_tournament(web3, deployed_contract, object_var):
	
	try:
		transact = deployed_contract.functions.addMatch(object_var).transact({'from': web3.eth.accounts[0]})
		settings.TX_RECEIPT.append(transact)
		receipt = web3.eth.wait_for_transaction_receipt(settings.TX_HASH)
		settings.TX_RECEIPT.append(receipt)
	except Exception as e:
		print(e)
	
	return

def get_tournament(web3, deployed_contract):
	values = []
	i = 0
	while True:
		try:
			value_get = deployed_contract.functions.getMatchIndex(web3.to_int(i)).call()
			if value_get == "No match found":
				break
			values.append(json.loads(value_get.replace("'", "\"")))
			i += 1
		except Exception as e:
			print(e)
			break
	return values

#TIPS: função para transformar querySet em json
def serialize_queryset(queryset: QuerySet) -> dict:
    def default(obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type '{obj.__class__.__name__}' is not JSON serializable")
    return json.loads(json.dumps(list(queryset), default=default))

def tournament(request):
	try:
		querySet_obj = Tournament.objects.all().order_by('-start_date')
		tournaments = serialize_queryset(querySet_obj.values())
		#TODO: por as var web3 e deployed_contract em um models para salvar o hash e o address
		if settings.BOOL_WEB3 == False:
			web3 = web3_init()
			deployed_contract = deploy_contract(web3)
			settings.BOOL_WEB3 = True

		#TODO: set precisa ser feito ao final de um torneio
		for i in range(len(tournaments)):
			set_tournament(web3, deployed_contract, str(tournaments[i]))

		#TIPS: GET pode ser feito nas visualizações dos torneios desde que haja um settings.TX_HASH
		# values = get_tournament(web3, deployed_contract)#TODO: set precisa ser feito ao final de um torneio
		# for i in range(len(tournaments)):

		# return render(request, 'tournaments/tournaments.html', {'tournament': values})
	except Exception as e:
		print("WEB3 Fail:", e)
		#TODO: dar um render em uma pagina de erro caso o container da blockchain nao suba
	return render(request, 'tournaments/tournaments.html', {'tournament': tournaments})
	

def tournament_4(request):
	if request.method == 'POST':
		turns = request.POST.get('qtd-turnos')
		user = get_object_or_404(CustomUser, username=request.user.username)
		friends = user.friends.all()
		return render(request, 'tournaments/tournament_4.html', {'user': user, 'friends': friends, 'turns': turns})


def tournament_8(request):
	if request.method == 'POST':
		total_players = request.POST.get('qtd-jogadores')
		turns = request.POST.get('qtd-turnos')
	return render(request, 'home.html')
