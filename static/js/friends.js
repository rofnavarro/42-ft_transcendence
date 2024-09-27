function togglePlayers(qtd) {
	if (qtd === 2) {
		document.getElementById('player3').style.display = 'none';
		document.getElementById('player4').style.display = 'none';
	} else {
		document.getElementById('player3').style.display = 'block';
		document.getElementById('player4').style.display = 'block';
	}
}

window.onload = function() {
	togglePlayers(2);
}

function openFriendModal() {
	document.getElementById('friend-modal').style.display = 'block';
}

function closeFriendModal() {
	document.getElementById('friend-modal').style.display = 'none';
}

function selectFriend(username) {

	closeFriendModal()
}