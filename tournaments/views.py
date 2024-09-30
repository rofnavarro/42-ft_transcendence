from .models import Tournament
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import QuerySet
from django.conf import settings
from users.models import CustomUser
import datetime
import json

from web3 import Web3
import json


def get_contract():
	with open('/home/rferrero/Desktop/transcendence/blockchain/hardhat/artifacts/contracts/Tournaments.sol/Tournament.json') as f:
		contract = json.load(f)
	return contract

def web3_init():
	contract = get_contract()
	web3Instance = Web3(Web3.HTTPProvider('http://localhost:8545/'))
	Tournament = web3Instance.eth.contract(abi=contract['abi'], bytecode=contract['bytecode'])
	account = web3Instance.eth.accounts[0]
	if settings.BOOL_WEB3 == False:
		try:
			if settings.TX_HASH == "BANANA1":
				settings.TX_HASH = (Tournament.constructor().transact({'from': account}))
			
			if settings.TX_ADDRESS == "BANANA2":
				settings.TX_RECEIPT.append(web3Instance.eth.wait_for_transaction_receipt(settings.TX_HASH))
				settings.TX_ADDRESS = settings.TX_RECEIPT[0].contractAddress

			settings.BOOL_WEB3 = True
		except Exception as e:
			print(e)
			pass
	deploy_contract(web3Instance)
	return (web3Instance)

def deploy_contract(web3):
	contract = get_contract()
	settings.DEPLOYED_CONTRACT = web3.eth.contract(address=settings.TX_ADDRESS, abi=contract['abi'])
	return ()

#---------------------------------------------

def serialize_queryset(queryset: QuerySet) -> dict:
    def default(obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type '{obj.__class__.__name__}' is not JSON serializable")
    return json.loads(json.dumps(list(queryset), default=default))

def set_tournament(tournament_id):
	tour = Tournament.objects.get(id=tournament_id)

	all_matches = tour.matches.all()

	object_match = []
	for match in all_matches:
		object_match.append(
			{
				"user1": match.user1.username,
				"user2": match.user2.username,
				"date": str(match.date),
				"score_user1": match.score_user1,
				"score_user2": match.score_user2,
				"winner": match.winner.username
			}
		)

	tournament_data = {
		"tournament": {
				"id": tour.id,
				"date": str(tour.date),
				"winner": tour.winner.username
			},
		"matches": object_match
	}

	object_var = json.dumps(tournament_data)
	web3 = web3_init()
	try:
		transact = settings.DEPLOYED_CONTRACT.functions.addMatch(object_var).transact({'from': web3.eth.accounts[0]})
		settings.TX_RECEIPT.append(transact)
		receipt = web3.eth.wait_for_transaction_receipt(settings.TX_HASH)
		settings.TX_RECEIPT.append(receipt)
	except Exception as e:
		print(e)
	
	print("blockchain values:", get_tournament(web3))

	return

def get_tournament(web3):
	web3 = web3_init()

	values = []
	i = 0
	while True:
		try:
			value_get = settings.DEPLOYED_CONTRACT.functions.getMatchIndex(web3.to_int(i)).call()
			if value_get == "No match found":
				break
			values.append(json.loads(value_get.replace("'", "\"")))
			i += 1
		except Exception as e:
			print(e)
			break
	return values


def tournaments(request):
	tournaments = Tournament.objects.all().order_by('-date')
	return render(request, 'tournaments/tournaments.html', { 'tournaments': tournaments })

	

def tournament_4(request):
	if request.method == 'POST':
		turns = request.POST.get('qtd-turnos')
		user = get_object_or_404(CustomUser, username=request.user.username)
		friends = user.friends.all()
		return render(request, 'tournaments/tournament_4.html', {'user': user, 'friends': friends, 'turns': turns})
