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
	new: function (side, username, nickname) {
		return {
			nickname: nickname,
			username: username,
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
	initialize: function (username1, username2, nickname1, nickname2, turns, match) {
		this.canvas = document.querySelector('canvas');
		this.context = this.canvas.getContext('2d');

		this.canvas.width = 2800;
		this.canvas.height = 1200;

		this.canvas.style.width = (this.canvas.width / 2) + 'px';
		this.canvas.style.height = (this.canvas.height / 2) + 'px';

		this.playerA = Computer.new.call(this, 'left', username1, nickname1);
		this.playerB = Computer.new.call(this, 'right', username2, nickname2);
		
		this.ball = Ball.new.call(this);

		this.running = this.over = false;
		this.turn = this.playerB;
		this.timer = this.round = 0;
		this.color = "#0A0A0A";

		this.roundsWonA = 0;
		this.roundsWonB = 0;
		this.pauseGame = false;	

		const _turns = parseInt(turns, 10);
		rounds = Array(_turns).fill(3);
		this.match = match;

		this.drawMenu();
		this.addEventListeners();
	},

	drawMenu: function () {
		this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
	
		this.context.fillStyle = this.color;
		this.context.fillRect(0, 0, this.canvas.width, this.canvas.height);

		this.context.font = '50px Dosis';
		this.context.textAlign = 'center';
		this.context.fillStyle = '#7B68EE';
		this.context.fillText('Press any key to begin', this.canvas.width / 2, this.canvas.height / 2 + 15);
	},

	endGameMenu: function (text) {
		this.resetBall();
		this.context.font = '45px Dosis';
		this.context.fillStyle = this.color;
		this.context.fillRect(this.canvas.width / 2 - 350, this.canvas.height / 2 - 48, 700, 100);
		this.context.fillStyle = '#7B68EE';
		this.context.fillText(text, this.canvas.width / 2, this.canvas.height / 2 + 15);
	
		if (this.match === '1'){
			document.getElementById('match-resultA-player').value = `${this.playerA.username}`;
			document.getElementById('match-resultA-score').value = `${this.roundsWonA}`;
			document.getElementById('match-resultB-player').value = `${this.playerB.username}`;
			document.getElementById('match-resultB-score').value = `${this.roundsWonB}`;
			const winner1 = document.getElementById('winner1');
			if (winner1) {
				winner1.value = `${this.roundsWonA > this.roundsWonB ? this.playerA.nickname : this.playerB.nickname}`;
			}
		}
		else if (this.match === '2'){
			document.getElementById('match-resultC-player').value = `${this.playerA.username}`;
			document.getElementById('match-resultC-score').value = `${this.roundsWonA}`;
			document.getElementById('match-resultD-player').value = `${this.playerB.username}`;
			document.getElementById('match-resultD-score').value = `${this.roundsWonB}`;
			const winner2 = document.getElementById('winner2');
			if (winner2) {
				winner2.value = `${this.roundsWonA > this.roundsWonB ? this.playerA.nickname : this.playerB.nickname}`;
			}
		}
	},

	addEventListeners: function () {
		document.addEventListener('keydown', (event) => {
			event.preventDefault();
			if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
				if (event.key === 'ArrowUp') this.playerB.move = DIRECTION.UP;
				if (event.key === 'ArrowDown') this.playerB.move = DIRECTION.DOWN;
			}
			if (event.key === 'w') this.playerA.move = DIRECTION.UP;
			if (event.key === 's') this.playerA.move = DIRECTION.DOWN;
			if (event.key === ' ' ) {
				this.pauseGame = false;
			}
			if (!this.running && !this.over) {
				this.running = true;
				this.startGame();
			}
		});

		document.addEventListener('keyup', (event) => {
			event.preventDefault();
			if (event.key === 'ArrowUp' || event.key === 'ArrowDown') this.playerB.move = DIRECTION.IDLE;
			if (event.key === 'w' || event.key === 's') this.playerA.move = DIRECTION.IDLE;
		});
	},

	startGame: function () {
		const gameLoop = () => {
			this.update();
			this.render();
			if (this.running && !this.over) {
				requestAnimationFrame(gameLoop);
			}
		};
		requestAnimationFrame(gameLoop);
	},

	update: function () {
		if (!this.over && !this.pauseGame) {
			this.handleBallCollisions();
			this.handlePlayerMovements();
			this.handleBallMovement();

			this.checkRoundEnd();
		}
		if (this.over === true)
		{
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
			this.pauseGame = true;
			this.roundsWonA++;
			if (!rounds[this.round + 1]) {
				this.over = true;
				this.resetBall();
				setTimeout(() => { this.endGameMenu(`${this.playerA.nickname} wins!`); }, 1000);
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
			this.pauseGame = true;
			this.roundsWonB++;
			if (!rounds[this.round + 1]) {
				this.over = true;
				this.resetBall();
				setTimeout(() => { this.endGameMenu(`${this.playerB.nickname} wins!`); }, 1000);
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
		this.ball.speed = 0;
		this.ball = Ball.new.call(this);
		this.ball.moveX = Math.random() > 0.5 ? DIRECTION.RIGHT : DIRECTION.LEFT;
		this.ball.moveY = Math.random() > 0.5 ? DIRECTION.DOWN : DIRECTION.UP;
	},

	render: function () {
		this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
	
		this.context.fillStyle = this.color;
		this.context.fillRect(0, 0, this.canvas.width, this.canvas.height);

		this.context.fillStyle = '#858cee';
		this.context.fillRect(this.playerA.x, this.playerA.y, this.playerA.width, this.playerA.height);
		this.context.fillRect(this.playerB.x, this.playerB.y, this.playerB.width, this.playerB.height);
		
		this.context.fillRect(this.canvas.width / 2 - 3, 60, 6, this.canvas.height - 120);

		this.context.beginPath();
		this.context.arc(this.ball.x + this.ball.width / 2, this.ball.y + this.ball.height / 2, this.ball.width / 2, 0, Math.PI * 2);
		this.context.fillStyle = '#ffffff';
		this.context.fill();
		this.context.closePath();

		this.context.font = '45px Dosis';
		this.context.fillStyle = '#7B68EE';
		this.context.fillText(this.playerA.score, this.canvas.width / 2 - 80, 50);
		this.context.fillText(this.playerB.score, this.canvas.width / 2 + 70, 50);

		this.context.font = '45px Dosis';
		this.context.fillStyle = '#7B68EE';
		this.context.fillText(`Round: ${this.round + 1} / ${rounds.length}`, this.canvas.width / 2, this.canvas.height - 20);
	
		this.context.fillText(`${this.playerA.nickname}: ${this.roundsWonA}`, 0 + 200, 50);
		this.context.fillText(`${this.playerB.nickname}: ${this.roundsWonB}`, this.canvas.width - 200, 50);

		if (this.pauseGame === true) {
			this.context.font = '45px Dosis';
			this.context.fillStyle = this.color;
			this.context.fillRect(this.canvas.width / 2 - 350, this.canvas.height / 2 - 48, 700, 100);
			this.context.fillStyle = '#7B68EE';
			this.context.fillText('Press "space" to continue', this.canvas.width / 2, this.canvas.height / 2 + 15);
		}

	},	
};

document.addEventListener('DOMContentLoaded', () => {
	
	Game.initialize(username1, username2, nickname1, nickname2, turns, match);
});
