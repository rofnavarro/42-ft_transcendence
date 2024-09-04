var DIRECTION = {
	IDLE: 0,
	UP: 1,
	DOWN: 2,
	LEFT: 3,
	RIGHT: 4
};

var rounds = [5, 5, 5];

var Ball = {
	new: function (incrementSpeed) {
		return {
			width: 18,
			height: 18,
			x: (this.canvas.width / 2) - 9,
			y: (this.canvas.height / 2) - 9,
			moveX: DIRECTION.IDLE,
			moveY: DIRECTION.IDLE,
			speed: incrementSpeed || 7
		};
	}
};

var Computer = {
	new: function (side) {
		return {
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
	initialize: function () {
		this.canvas = document.querySelector('canvas');
		this.context = this.canvas.getContext('2d');

		this.canvas.width = 1400;
		this.canvas.height = 1000;

		this.canvas.style.width = (this.canvas.width / 2) + 'px';
		this.canvas.style.height = (this.canvas.height / 2) + 'px';

		this.playerA = Computer.new.call(this, 'left');
		this.playerB = Computer.new.call(this, 'right');
		this.ball = Ball.new.call(this);

		this.running = this.over = false;
		this.turn = this.playerB;
		this.timer = this.round = 0;
		this.color = '#0a0a0a';

		Pong.menu();
		Pong.listen();
	},

	endGameMenu: function (text) {
		Pong.context.font = '45px Dosis';
		Pong.context.fillStyle = this.color;

		Pong.context.fillRect(
			Pong.canvas.width / 2 - 350,
			Pong.canvas.height / 2 - 48,
			700,
			100
		);

		Pong.context.fillStyle = '#858cee';

		Pong.context.fillText(text,
			Pong.canvas.width / 2,
			Pong.canvas.height / 2 + 15
		);

		setTimeout(function () {
			Pong = Object.assign({}, Game);
			Pong.initialize();
		}, 3000);
	},

	menu: function () {
		Pong.draw();

		this.context.font = '50px Dosis';
		this.context.fillStyle = this.color;

		this.context.fillRect(
			this.canvas.width / 2 - 350,
			this.canvas.height / 2 - 48,
			700,
			100
		);

		this.context.fillStyle = '#858cee';

		this.context.fillText('Press any key to begin',
			this.canvas.width / 2,
			this.canvas.height / 2 + 15
		);
	},

	update: function () {
		if (!this.over) {
			if (this.ball.x <= 0) Pong._resetTurn.call(this, this.playerB, this.playerA);
			if (this.ball.x >= this.canvas.width - this.ball.width) Pong._resetTurn.call(this, this.playerA, this.playerB);
			if (this.ball.y <= 0) this.ball.moveY = DIRECTION.DOWN;
			if (this.ball.y >= this.canvas.height - this.ball.height) this.ball.moveY = DIRECTION.UP;

			if (this.playerA.move == DIRECTION.UP) this.playerA.y -= this.playerA.speed;
			else if (this.playerA.move == DIRECTION.DOWN) this.playerA.y += this.playerA.speed;

			if (this.playerB.move == DIRECTION.UP) this.playerB.y -= this.playerB.speed;
			else if (this.playerB.move == DIRECTION.DOWN) this.playerB.y += this.playerB.speed;

			if (Pong._turnDelayIsOver.call(this) && this.turn) {
				this.ball.moveX = this.turn === this.playerA ? DIRECTION.LEFT : DIRECTION.RIGHT;
				this.ball.moveY = [DIRECTION.UP, DIRECTION.DOWN][Math.floor(Math.random() * 2)];
				this.ball.y = Math.floor(Math.random() * (this.canvas.height - 200)) + 100;
				this.turn = null;
			}

			if (this.playerA.y <= 0) this.playerA.y = 0;
			else if (this.playerA.y >= (this.canvas.height - this.playerA.height)) this.playerA.y = (this.canvas.height - this.playerA.height);

			if (this.playerB.y <= 0) this.playerB.y = 0;
			else if (this.playerB.y >= (this.canvas.height - this.playerB.height)) this.playerB.y = (this.canvas.height - this.playerB.height);

			if (this.ball.moveY === DIRECTION.UP) this.ball.y -= (this.ball.speed / 1.5);
			else if (this.ball.moveY === DIRECTION.DOWN) this.ball.y += (this.ball.speed / 1.5);

			if (this.ball.moveX === DIRECTION.LEFT) this.ball.x -= this.ball.speed;
			else if (this.ball.moveX === DIRECTION.RIGHT) this.ball.x += this.ball.speed;

			if (this.ball.x - this.ball.width <= this.playerA.x + this.playerA.width &&
				this.ball.y + this.ball.height >= this.playerA.y &&
				this.ball.y <= this.playerA.y + this.playerA.height) {

					var collideY = (this.ball.y + this.ball.height / 2) - (this.playerA.y + this.playerA.height / 2);
					var collideRatio = collideY / (this.playerA.height / 2);
					var angle = collideRatio * (Math.PI / 4);

					this.ball.moveX = DIRECTION.RIGHT;
					this.ball.moveY = (angle > 0) ? DIRECTION.DOWN : DIRECTION.UP;
					this.ball.x = this.playerA.x + this.playerA.width;
					this.ball.speed += 0.25;
				}

			if (this.ball.x + this.ball.width >= this.playerB.x &&
				this.ball.y + this.ball.height >= this.playerB.y &&
				this.ball.y <= this.playerB.y + this.playerB.height) {

					var collideY = (this.ball.y + this.ball.height / 2) - (this.playerB.y + this.playerB.height / 2);
					var collideRatio = collideY / (this.playerB.height / 2);
					var angle = collideRatio * (Math.PI / 4);

					this.ball.moveX = DIRECTION.LEFT;
					this.ball.moveY = (angle > 0) ? DIRECTION.DOWN : DIRECTION.UP;
					this.ball.x = this.playerB.x - this.ball.width;
					this.ball.speed += 0.25;
				}
		}

			if (this.playerA.score === rounds[this.round]) {
				if (!rounds[this.round + 1]) {
					this.over = true;
					setTimeout(function () { Pong.endGameMenu('PlayerA wins!'); }, 1000 );
				} else {
					this.playerA.score = this.playerB.score = 0;
					this.playerA.speed += 1;
					this.playerB.speed += 1;
					this.ball.speed += 0.5;
					this.round += 1;
				}
			}
			else if (this.playerB.score === rounds[this.round]) {
				this.over = true;
				setTimeout(function () { Pong.endGameMenu('PlayerB wins!'); }, 1000);
			}
		},

		draw: function () {
			this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);

			this.context.fillStyle = this.color;
			this.context.fillRect(0, 0, this.canvas.width, this.canvas.height);

			this.context.fillStyle = '#858cee';
			this.context.fillRect(this.playerA.x, this.playerA.y, this.playerA.width, this.playerA.height);
			this.context.fillRect(this.playerB.x, this.playerB.y, this.playerB.width, this.playerB.height);

			if (Pong._turnDelayIsOver.call(this)) {
				this.context.beginPath();
				this.context.arc(this.ball.x + this.ball.width / 2, this.ball.y + this.ball.height / 2, this.ball.width / 2, 0, 2 * Math.PI);
				this.context.fillStyle = '#858cee';
				this.context.fill();
			}

			this.context.beginPath();
			this.context.setLineDash([7, 15]);
			this.context.moveTo(this.canvas.width / 2, this.canvas.height - 140);
			this.context.lineTo(this.canvas.width / 2, 140);
			this.context.lineWidth = 10;
			this.context.strokeStyle = '#858cee';
			this.context.stroke();

			this.context.font = '100px Dosis';
			this.context.textAlign = 'center';

			this.context.fillText(this.playerA.score.toString(), (this.canvas.width / 2) - 300, 200);
			this.context.fillText(this.playerB.score.toString(), (this.canvas.width / 2) + 300, 200);

			this.context.font = '40px Dosis';
			this.context.fillText('Round ' + (Pong.round + 1), (this.canvas.width / 2), 35);
			this.context.fillText(rounds[Pong.round] ? rounds[Pong.round] : rounds[Pong.round - 1], (this.canvas.width / 2), 100);
		},

		loop: function () {
			Pong.update();
			Pong.draw();

			if (!Pong.over) requestAnimationFrame(Pong.loop);
		},

		listen: function () {
			document.addEventListener('keydown', function(key) {
				if (Pong.running === false) {
					Pong.running = true;
					window.requestAnimationFrame(Pong.loop);
				}

				if (key.keyCode === 87) Pong.playerA.move = DIRECTION.UP;
				if (key.keyCode === 38) Pong.playerB.move = DIRECTION.UP;
				if (key.keyCode === 83) Pong.playerA.move = DIRECTION.DOWN;
				if (key.keyCode === 40) Pong.playerB.move = DIRECTION.DOWN;

				event.preventDefault();
			});

			document.addEventListener('keyup', function(key) {
				if (key.keyCode === 38 || key.keyCode === 40) {
					Pong.playerB.move = DIRECTION.IDLE;
				}
				Pong.playerA.move = DIRECTION.IDLE;
			});
		},

		_resetTurn: function(winner, loser) {
			this.ball = Ball.new.call(this, this.ball.speed);
			this.turn = loser;
			this.timer = (new Date()).getTime();

			winner.score++;
		},

		_turnDelayIsOver: function() {
			return ((new Date()).getTime() - this.timer >= 1000);
		},
	};

	var Pong = Object.assign({}, Game);
	Pong.initialize();