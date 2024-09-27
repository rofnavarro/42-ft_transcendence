var DIRECTION = {
	IDLE: 0,
	UP: 1,
	DOWN: 2,
	LEFT: 3,
	RIGHT: 4
};

var rounds = [];

var Ball = {
	new: function (incrementSpeed) {
		return {
			width: 18,
			height: 18,
			x: (this.canvas.width / 2) - 9,
			y: (this.canvas.height / 2) - 9,
			moveX: Math.random() > 0.5 ? DIRECTION.RIGHT : DIRECTION.LEFT,
			moveY: Math.random() > 0.5 ? DIRECTION.DOWN : DIRECTION.UP,
			speed: incrementSpeed || 7
		};
	}
};

var Computer = {
	new: function (side, player_name, player_username) {
		return {
			name: player_name,
			username: player_username,
			width: 18,
			height: 180,
			x: side === 'left' ? 150 : this.canvas.width - 150,
			y: (this.canvas.height / 2) - 35,
			score: 0,
			move: DIRECTION.IDLE,
			speed: 8
		};
	}
};

var Game = {
	initialize: function (players, usernames, turns, color) {
		this.canvas = document.querySelector('canvas');
		this.context = this.canvas.getContext('2d');

		this.canvas.width = 2800;
		this.canvas.height = 1200;

		this.canvas.style.width = (this.canvas.width / 2) + 'px';
		this.canvas.style.height = (this.canvas.height / 2) + 'px';

		this.playerA = Computer.new.call(this, 'left', players[0], usernames[0]);
		this.playerB = Computer.new.call(this, 'right', players[1], usernames[1]);
		
		this.ball = Ball.new.call(this);

		this.running = this.over = this.matchSaved = false;
		this.turn = this.playerB;
		this.timer = this.round = 0;
		this.color = color;

		this.roundsWonA = 0;
		this.roundsWonB = 0;	

		const _turns = parseInt(turns, 10);
		rounds = Array(_turns).fill(3);

		this.drawMenu();
		this.addEventListeners();
	},

	drawMenu: function () {
		this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
	
		this.context.fillStyle = this.color;
		this.context.fillRect(0, 0, this.canvas.width, this.canvas.height);

		this.context.font = '50px Dosis';
		this.context.textAlign = 'center';
		this.context.fillStyle = '#858cee';
		this.context.fillText('Press any key to begin', this.canvas.width / 2, this.canvas.height / 2 + 15);
	},

	endGameMenu: function (text) {
		this.context.font = '45px Dosis';
		this.context.fillStyle = this.color;
		this.context.fillRect(this.canvas.width / 2 - 350, this.canvas.height / 2 - 48, 700, 100);
		this.context.fillStyle = '#858cee';
		this.context.fillText(text, this.canvas.width / 2, this.canvas.height / 2 + 15);
	},

	addEventListeners: function () {
		document.addEventListener('keydown', (event) => {
			if (event.key === 'ArrowUp') this.playerB.move = DIRECTION.UP;
			if (event.key === 'ArrowDown') this.playerB.move = DIRECTION.DOWN;
			if (event.key === 'w') this.playerA.move = DIRECTION.UP;
			if (event.key === 's') this.playerA.move = DIRECTION.DOWN;

			if (!this.running && !this.over) {
				this.running = true;
				this.startGame();
			}
		});

		document.addEventListener('keyup', (event) => {
			if (event.key === 'ArrowUp' || event.key === 'ArrowDown') this.playerB.move = DIRECTION.IDLE;
			if (event.key === 'w' || event.key === 's') this.playerA.move = DIRECTION.IDLE;
		});
	},

	startGame: function () {
		this.timer = setInterval(() => {
			this.update();
			this.render();
		}, 1000 / 60);
	},

	update: function () {
		if (!this.over) {
			this.handleBallCollisions();
			this.handlePlayerMovements();
			this.handleBallMovement();

			this.checkRoundEnd();
		}
		if (this.over === true && this.matchSaved === false)
		{
			saveMatch(this.playerA.name, this.playerB.name, this.roundsWonA, this.roundsWonB);
			this.matchSaved = true;
			return;
		}
	},
	
	detectCollision: function (ball, player) {
		const nextBallX = ball.x + (ball.moveX === DIRECTION.RIGHT ? ball.speed : (ball.moveX === DIRECTION.LEFT ? -ball.speed : 0));
		const nextBallY = ball.y + (ball.moveY === DIRECTION.UP ? ball.speed : (ball.moveY === DIRECTION.DOWN ? +ball.speed : 0));

		return (nextBallX < player.x + player.width &&
				nextBallX + ball.width > player.x &&
				nextBallY < player.y + player.height &&
				nextBallY + ball.height > player.y);
	},

	handleBallCollisions: function () {
		if (this.ball.x - (this.ball.width / 2) <= 0) this.resetTurn(this.playerB, this.playerA);
		if (this.ball.x + (this.ball.width / 2) >= this.canvas.width) this.resetTurn(this.playerA, this.playerB);
		if (this.ball.y - (this.ball.height / 2) <= 0) this.ball.moveY = DIRECTION.DOWN;
		if (this.ball.y + (this.ball.height) >= this.canvas.height) this.ball.moveY = DIRECTION.UP;

		if (this.detectCollision(this.ball, this.playerA)) {
			this.handlePlayerCollision(this.playerA, DIRECTION.RIGHT);
		}

		if (this.detectCollision(this.ball, this.playerB)) {
			this.handlePlayerCollision(this.playerB, DIRECTION.LEFT);
		}
	},

	handlePlayerCollision: function (player, newMoveX) {
		const collideY = (this.ball.y + this.ball.height / 2) - (player.y + player.height / 2);
		const collideRatio = collideY / (player.height / 2);
		const angle = collideRatio * (Math.PI / 4);

		this.ball.moveX = newMoveX;
		this.ball.moveY = (angle > 0) ? DIRECTION.DOWN : DIRECTION.UP;
		this.ball.speed += 0.25;

		if (newMoveX === DIRECTION.RIGHT) {
			this.ball.x = player.x + player.width;
		} else {
			this.ball.x = player.x - this.ball.width;
		}
	},

	handlePlayerMovements: function () {
		if (this.playerA.move === DIRECTION.UP) this.playerA.y -= this.playerA.speed;
		if (this.playerA.move === DIRECTION.DOWN) this.playerA.y += this.playerA.speed;
		if (this.playerB.move === DIRECTION.UP) this.playerB.y -= this.playerB.speed;
		if (this.playerB.move === DIRECTION.DOWN) this.playerB.y += this.playerB.speed;

		this.playerA.y = Math.max(0, Math.min(this.canvas.height - this.playerA.height, this.playerA.y));
		this.playerB.y = Math.max(0, Math.min(this.canvas.height - this.playerB.height, this.playerB.y));
	},

	handleBallMovement: function () {
		if (this.ball.moveY === DIRECTION.UP) this.ball.y -= this.ball.speed;
		if (this.ball.moveY === DIRECTION.DOWN) this.ball.y += this.ball.speed;
		if (this.ball.moveX === DIRECTION.LEFT) this.ball.x -= this.ball.speed;
		if (this.ball.moveX === DIRECTION.RIGHT) this.ball.x += this.ball.speed;
	},

	checkRoundEnd: function () {
		if (this.playerA.score === rounds[this.round]) {
			this.roundsWonA++;
			if (!rounds[this.round + 1]) {
				this.over = true;
				this.resetBall();
				setTimeout(() => { this.endGameMenu('Player 1 wins!'); }, 10000);
			} else {
				this.playerA.score = this.playerB.score = 0;
				this.playerA.speed += 1;
				this.playerB.speed += 1;
				this.round++;
				this.resetBall();
				this.turn = this.playerB;
			}
		}
		else if (this.playerB.score === rounds[this.round]) {
			this.roundsWonB++;
			if (!rounds[this.round + 1]) {
				this.over = true;
				this.resetBall();
				setTimeout(() => { this.endGameMenu('Player 2 wins!'); }, 10000);
			} else {
				this.playerA.score = this.playerB.score = 0;
				this.playerA.speed += 1;
				this.playerB.speed += 1;
				this.round++;
				this.resetBall();
				this.turn = this.playerA;
			}
		}
	},

	resetTurn: function (scoringPlayer, nextPlayer) {
		scoringPlayer.score++;
		this.resetBall();
		this.turn = nextPlayer;
	},

	resetBall: function () {
		this.ball = Ball.new.call(this);
		this.ball.moveX = Math.random() > 0.5 ? DIRECTION.RIGHT : DIRECTION.LEFT;
		this.ball.moveY = Math.random() > 0.5 ? DIRECTION.DOWN : DIRECTION.UP;
		this.ball.speed = 7;
	},

	render: function () {
		this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
	
		this.context.fillStyle = this.color;
		this.context.fillRect(0, 0, this.canvas.width, this.canvas.height);

		this.context.fillStyle = '#858cee';
		this.context.fillRect(this.playerA.x, this.playerA.y, this.playerA.width, this.playerA.height);
		this.context.fillRect(this.playerB.x, this.playerB.y, this.playerB.width, this.playerB.height);

		this.context.fillStyle = '#ffffff';
		this.context.fillRect(this.ball.x, this.ball.y, this.ball.width, this.ball.height);

		this.context.font = '40px Dosis';
		this.context.fillStyle = '#858cee';
		this.context.fillText(this.playerA.score, this.canvas.width / 2 - 80, 50);
		this.context.fillText(this.playerB.score, this.canvas.width / 2 + 50, 50);

		this.context.font = '40px Dosis';
		this.context.fillStyle = '#858cee';
		this.context.fillText(`Round: ${this.round + 1} / ${rounds.length}`, this.canvas.width / 2, this.canvas.height - 20);
	
		this.context.fillText(`${this.playerA.username}: ${this.roundsWonA}`, 0 + 200, 50);
		this.context.fillText(`${this.playerB.username}: ${this.roundsWonB}`, this.canvas.width - 200, 50);

	}
};

document.addEventListener('DOMContentLoaded', () => {
	Game.initialize(players, usernames, turns, color, csrfToken);
});

function saveMatch(user1, user2, roundsWonA, roundsWonB) {
	
	const data = {
		user1: user1,
		user2: user2,
		score_user1: roundsWonA,
		score_user2: roundsWonB
	};

	const csrftoken = getCookie('csrftoken');

	fetch('/match/save_match_ajax', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
		body: JSON.stringify(data)
	})
	.then(response => response.json())
	.then(data => {
		if (data.status === 'success') {
		} else {
			console.error('Error saving match:', data.message);
		}
	})
	.catch(error => console.error('Error:', error));
}

function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}