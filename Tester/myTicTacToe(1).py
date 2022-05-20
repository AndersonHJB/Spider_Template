import random

"""
Author: Ka Wai Lau
Date: May 2021
Version: 3.4

Fix bugs and increase speed of learning by simplifying internal representation
of game state.
"""

# CONSTANTS

RL_AGENT = 1
RANDOM_AGENT = 2
HUMAN_AGENT = 3
MINIMAX_AGENT = 4
TRAINING_MODE = 5
PLAYING_MODE = 6

# Set random number seed here
random.seed(20021007)


def createPlayer(letter, playerType=RANDOM_AGENT):
	"""
	This function creates a player and assigns it a letter

	:param letter: The players letter; single character X or O
	:type letter: String
	:param playerType: The type of player to create, must be RL_AGENT, RANDOM_AGENT, HUMAN_AGENT or MINIMAX_AGENT
	:type playerType: Integer
	:return: Player, RLPlayer, MINIPlayer or HUMANPlayer
	"""

	if playerType == RL_AGENT:
		return RLPlayer(letter, playerType)
	elif playerType == HUMAN_AGENT:
		return HUMANPlayer(letter, playerType)
	elif playerType == MINIMAX_AGENT:
		return MINIPlayer(letter, playerType)

	return Player(letter, playerType)

def train(player1, player2, episodes):
	"""
	This function executes n (episodes) tictactoe games.  Player 1 or 2 must be
	an RL agent.  The RL agent has to play against another player to learn how
	to play.  The second player should be a RANDOM player.

	:param player1: An RL or RANDOM agent.
	:type player1: Player or RLPlayer
	:param player2: An RL or RANDOM agent.
	:type player2: Player or RLPlayer
	:param episodes: Number of episodes to execute
	:type episodes: Integer
	"""

	for i in range(episodes) :
		board = TicTacToe()
		board.setPlayers(player1, player2)
		runEpisode(board)

def runEpisode(board) :
	"""
	This method executes a single tictactoe game and updates
	the state value table after every move played by the RL agent.

	:param board: The tictactoe game board
	:type board: TicTacToe
	"""

	players = board.getPlayers()
	rlplayer = players[0]

	if not rlplayer.getType() == RL_AGENT:
		rlplayer = players[1]

	rlplayer.previousState = board.copy()
	while not board.isGameOver():

		player = board.next()
		player.makeMove(board)

	rlplayer.rewardState(board)


class TicTacToe :
	"""
	This class represents the TicTacToe board. It draws the board and keeps track
	of the moves that have been made.
	"""

	def __init__(self) :
		"""
		This is the constructor.  It creates a new empty board. Internally,
		the board is a 2D list.  Empty squares are denotes with a single
		asterisk '*'
		"""

		self.board = ['*', '*', '*', '*', '*', '*', '*', '*', '*']
		self.moveCount = 0
		self.lastMove = None
		self.remainingMoves = [0,1,2,3,4,5,6,7,8]
		self.player1 = None
		self.player2 = None
		self.userQuit = False

	def setPlayers(self, player1, player2):
		"""
		Sets the players

		:param player1: Player 1
		:type player1: Player, RLPlayer, MINIPlayer or HUMANPlayer
		:param player2: Player 2
		:type player2: Player, RLPlayer, MINIPlayer or HUMANPlayer
		"""

		self.player1 = player1
		self.player2 = player2

		self.player1.winner = False
		self.player2.winner = False

		self.player1.isTurn = True
		self.player2.isTurn = False

	def getPlayers(self):
		"""
		Gets the players

		:return: List of Players
		"""
		return [self.player1, self.player2]

	def next(self):
		"""
		Gets the next player to go

		:return: Player, RLPlayer, MINIPlayer or HUMANPlayer
		"""

		if self.player1.isTurn:
			self.player1.isTurn = False
			self.player2.isTurn = True
			return self.player1
		else:
			self.player1.isTurn = True
			self.player2.isTurn = False
			return self.player2

	def getWinner(self):
		"""
		Gets the player that won the game

		:return: Player, RLPlayer, MINIPlayer, HUMANPlayer or None
		"""
		if self.isGameWon(self.player1.letter):
			return self.player1
		elif self.isGameWon(self.player2.letter):
			return self.player2
		elif self.isGameDraw() or self.userQuit:
			return None

	def isGameOver(self) :
		"""
		This method determines if the game is over.  Returns True if someone has won
		or the game is drawn, otherwise it returns False

		:return: True or False
		"""

		if self.isGameWon('X'):
			return True

		if self.isGameWon('O'):
			return True

		if self.userQuit:
			return True

		if self.moveCount >= 9:
			return True

		return False


	def isGameDraw(self) :
		"""
		This method determines if the game is a draw.  Returns True if game is a
		draw (no has won), otherwise it returns False

		:return: True or False
		"""

		if self.moveCount >= 9:
			return True

		return False

	def isGameWon(self, mark):
		"""
		This method checks to see if a player, specified by mark, has won the
		game.  It returns True if 'mark' has won the game, other False

		:param mark: A letter, e.g., 'X' or 'O'
		:type mark: String
		:return: True or False
		"""

		if self.isSameAs(mark, self.board[0], self.board[1], self.board[2]):
			return True

		if self.isSameAs(mark, self.board[3], self.board[4], self.board[5]):
			return True

		if self.isSameAs(mark, self.board[6], self.board[7], self.board[8]):
			return True

		if self.isSameAs(mark, self.board[0], self.board[3], self.board[6]):
			return True

		if self.isSameAs(mark, self.board[1], self.board[4], self.board[7]):
			return True

		if self.isSameAs(mark, self.board[2], self.board[5], self.board[8]):
			return True

		if self.isSameAs(mark, self.board[0], self.board[4], self.board[8]):
			return True

		if self.isSameAs(mark, self.board[2], self.board[4], self.board[6]):
			return True

		return False

	def isSameAs(self, char, a, b, c):
		"""
		This methods checks if all four parameters are equal.  Returns True if
		all four characters are the same otherwise False.

		:param char:  A character, e.g., 'X' or 'O'
		:type char: String
		:param a: A character, e.g., 'X' or 'O' or '*'
		:type a: String
		:param b: A character, e.g., 'X' or 'O' or '*'
		:type b: String
		:param c: A character, e.g., 'X' or 'O' or '*'
		:type c: String
		:return: True or False
		"""

		if char == a and a == b and b == c:
			return True

		return False

	def drawBoard(self):
		"""
		This method displays the game on the screen.  It can only display the
		letters X and O.
		"""

		letterX = ['  X     X  ', '   X   X   ', '    X X    ', \
					'     X     ', '    X X    ', '   X   X   ', '  X     X  ']
		letterO = ['   OOOOO   ', '  O     O  ', '  O     O  ', \
					'  O     O  ', '  O     O  ', '  O     O  ', '   OOOOO   ']

		tmp = []
		tmp.append((' ' * 11) + '@' + (' ' * 11) + '@' + (' ' * 11))
		lim = [[0,3], [3,6], [6,9]]

		for i in range(3):
			# row = self.board[i]
			limits = lim[i]
			row = self.board[limits[0]:limits[1]]

			for j in range(7):
				msg = ""
				for k in range(3):
					if row[k] == 'X':
						msg += letterX[j]
					elif row[k] == 'O':
						msg += letterO[j]
					else:
						msg += ' ' * 11

					if k != 2:
						msg += '@'

				tmp.append(msg)

			if i != 2:
				tmp.append((' ' * 11) + '@' + (' ' * 11) + '@' + (' ' * 11))
				tmp.append('@' * 35)
				tmp.append((' ' * 11) + '@' + (' ' * 11) + '@' + (' ' * 11))

		tmp.append((' ' * 11) + '@' + (' ' * 11) + '@' + (' ' * 11))
		print("\n\n")
		for line in tmp:
			print(line)
		print("\n\n")

	def makeMove(self, location, mark):
		"""
		This method puts a letter (mark) on the board, at location, if it's
		legal to do so.  Returns True if the location is valid and the square
		has not been marked already; False for all other conditions

		:param location: An Integer between 0 - 8
		:type location: Integer
		:param mark: The letter, 'X' or 'O'
		:type mark: String
		:return: True or False
		"""

		if 0 <= location <= 8:

			if self.board[location] != '*':
				return False

			self.board[location] = mark
			self.moveCount += 1
			self.lastMove = location

			self.remainingMoves.remove(location)

			return True

		return False

	def copy(self) :
		"""
		This method makes a copy of the tictactoe board.  Returns a new
		Tictactoe board.

		:return: TicTacToe
		"""

		newBoard = TicTacToe()

		newBoard.board = self.board[:]
		newBoard.moveCount = self.moveCount
		newBoard.lastMove = self.lastMove
		newBoard.remainingMoves = self.remainingMoves[:]
		newBoard.player1 = self.player1
		newBoard.player2 = self.player2
		newBoard.userQuit = self.userQuit

		return newBoard

	def getKey(self, letter):
		"""
		This method transforms the list which represents the board into
		a single string to be used as a key. In the key, the Xs and Os are
		replaced with L and T where L represents the letter (X or O) used
		by the learning agent and the T is the opponent. This allows
		the agent to learn by playing as X or O.  Returns a string, 9 characters
		long, of Ls, Ts and asterisks.

		:param letter: the letter used by the learning agent.
		:type letter: String
		:return: String
		"""

		r = "".join(self.board)

		r = r.replace(letter, 'L')
		if letter == 'X' :
			r = r.replace('O', 'T')
		else:
			r = r.replace('X', 'T')

		return r


class Player :
	"""
	This class represents a person or agent playing tictactoe.
	"""

	def __init__(self, letter, playerType=RANDOM_AGENT) :
		"""
		When creating a Player you have to specify a letter and player type.
		The letter is either 'X' or 'O' (both capitilised).  The player type can
		be: RL_AGENT, RANDOM_AGENT, HUMAN_AGENT, or MINIMAX_AGENT. The default
		is RANDOM_AGENT.

		:param letter: The letter the player uses, can only be 'X' or 'O'
		:type letter: String
		:param playerType: The type of player 'HUMAN', 'MINIMAX', 'RL' OR 'RANDOM'
		:type playerType: Integer
		"""

		self.letter = letter
		self.opponent = 'O'

		if letter == 'O':
			self.opponent = 'X'

		self.playerType = playerType

		self.name = "Unknown"
		self.rating = 1200
		self.gamesW = 0
		self.gamesD = 0
		self.gamesL = 0

		self.firstPlayer = True
		self.isTurn = True
		self.winner = False

	def getType(self):
		"""
		Gets the player's type

		:return: RL_AGENT, RANDOM_AGENT, HUMAN_AGENT or MINIMAX_AGENT
		"""
		return self.playerType

	def makeMove(self, board):
		"""
		Selects a random move.

		:param board: The tictactoe game board
		:type board: TicTacToe
		"""

		moveLegal = False

		while not moveLegal:
			loc = random.randint(0,8)
			moveLegal = board.makeMove(loc, self.letter)


class RLPlayer(Player) :
	"""
	This class represents a Reinforcement Learning agent.
	"""

	def __init__(self, letter, playerType=RL_AGENT) :
		"""
		When creating an RLPlayer you must specify a letter, either 'X' or 'O'
		(both capitilised).  Do not specify the playerType.

		:param letter: The letter the player uses, can only be 'X' or 'O'
		:type letter: String
		:param playerType: RL_AGENT
		:type playerType: Integer
		"""

		super().__init__(letter, playerType)

		self.learningRate = 0.0
		self.discountRate = 0.0
		self.epsilon = 0.0
		self.valueFunction = {}
		self.previousState = None
		self.mode = PLAYING_MODE

	def initTraining(self, learning, discount, epsilon):
		"""
		This method initialises the RL agent's learning parameters.

		:param learning: Learning rate
		:type learning: Float
		:param discount: Discount rate
		:type discount: Float
		:param epsilon: Epsilon (epsilon-Greedy Algorithm)
		:type epsilon: Float
		"""

		self.learningRate = learning
		self.discountRate = discount
		self.epsilon = epsilon
		self.previousState = None
		self.mode = TRAINING_MODE

	def setMode(self, mode):
		"""
		This method sets the RL agent's mode:

		:param mode: The RL agent's mode
		:type mode: TRAINING_MODE or PLAYING_MODE
		"""
		self.mode = mode

	def getMode(self):
		"""
		This method gets the RL agent's mode:

		:return: TRAINING_MODE or PLAYING_MODE
		"""

		return self.mode

	def makeMove(self, board):
		"""
		This method is responsible for making a move for the RL agent.
		It follows the Epsilon-Greedy Algorithm which balances the need for
		exploitation and exploration.

		:param board: The tictactoe game board
		:type board: TicTacToe
		"""

		# *** NOT IMPLEMENTED YET!! ***

		if self.getMode() == TRAINING_MODE:
			n = random.uniform(0, 1)

			if n < self.epsilon:
				anyMove = random.choice(board.remainingMoves)
				moveLegal = board.makeMove(anyMove, self.letter)

				if not moveLegal:
					print('*** WARNING ILLEGAL MOVE BY RL ***')

			else:
				self.getRLMove(board)
			self.rewardState(board, self.previousState)
			self.previousState = board.copy()

		else:
			self.getRLMove(board)

	def rewardState(self, board, prevBoard=None):
		"""
		This method updates the policy (the valueFunction dictionary)

		:param board: The tictactoe game board
		:type board: TicTacToe
		:param prevBoard: The previous tictactoe game board
		:type prevBoard: TicTacToe
		"""

		# *** NOT IMPLEMENTED YET!! ***

		if prevBoard is None:
			reward = self.getReward(board)
			key = board.getKey(self.letter)
			value = self.valueOfState(key)
			self.valueFunction[key] = value + self.learningRate * reward
		else:
			reward = self.getReward(board)
			key = board.getKey(self.letter)
			value = self.valueOfState(key)

			keyPrev = prevBoard.getKey(self.letter)
			valuePrev = self.valueOfState(keyPrev)
			self.valueFunction[keyPrev] = valuePrev + self.learningRate * (reward +(self.discountRate * value) - valuePrev)


	def getRLMove(self, board) :
		"""
		This method performs moves for the RL agent while it's in training. It
		will either select a move at random (for exploration) or select the best
		move according to the state value table (for exploitation).

		:param board: The tictactoe game board
		:type board: TicTacToe
		"""

		bestMove = None
		bestValue = -99999

		for location in board.remainingMoves:
			cboard = board.copy()
			cboard.makeMove(location, self.letter)
			key = cboard.getKey(self.letter)

			if key in self.valueFunction :
				if self.valueFunction[key] >= bestValue :
					bestValue = self.valueFunction[key]
					bestMove = location

		if bestMove is not None:
			move = bestMove
		else:
			move = random.choice(board.remainingMoves)

		moveLegal = board.makeMove(move, self.letter)

		if not moveLegal:
			print('*** WARNING ILLEGAL MOVE BY RL ***')

	def valueOfState(self, key) :
		"""
		This method returns the value of a state; helper method

		:param key: The state of the game board
		:type key: String
		:return: Float
		"""

		if key in self.valueFunction :
			return self.valueFunction[key]
		else :
			self.valueFunction[key] = 0
			return 0

	def getReward(self, board) :
		"""
		This method will be implemented by the student as part of the lab.  It
		analyses the board and determines a reward.  The exact reward scheme
		will be designed by the student.

		:param board: The tictactoe game board
		:type board: TicTacToe
		:return: Integer
		"""

		# *** NOT IMPLEMENTED YET!! ***

		if board.getWinner() is None:
			return 5
		elif board.getWinner().letter == self.letter:
			return 10
		else:
			return 0




class MINIPlayer(Player) :

	"""
	This class represents a MiniMax player.
	"""

	def __init__(self, letter, playerType=MINIMAX_AGENT) :
		"""
		When creating a MINIPlayer you must specify a letter, either 'X' or 'O'
		(both capitilised).  Do not specify the playerType.

		:param letter: The letter the player uses, can only be 'X' or 'O'
		:type letter: String
		:param playerType: MINIMAX_AGENT
		:type playerType: Integer
		"""

		super().__init__(letter, playerType)


	def makeMove(self, board):
		"""
		This method performs a move for the Minimax player.

		:param board: The tictactoe game board
		:type board: TicTacToe
		"""

		playerMove = self.minimax(board)
		moveLegal = board.makeMove(playerMove, self.letter)

		if not moveLegal:
			print('*** WARNING ILLEGAL MOVE BY MINIMAX ***')

	def minimax(self, board):
		"""
		This method will be implemented by the student as part of the lab. It
		uses a recursive helper method to search the game tree for an optimal
		move.  It returns the best possible move.

		:param board: The tictactoe game board
		:type board: TicTacToe
		:return: Integer
		"""

		# *** NOT IMPLEMENTED YET!! ***

		children = board.remainingMoves
		bestScore = -999
		bestMove = None

		for move in children:
			copyBoard = board.copy()
			copyBoard.makeMove(move, self.letter)
			score = self.minimaxHelper(copyBoard, False)
			if score > bestScore:
				bestScore = score
				bestMove = move

		return bestMove


	def minimaxHelper(self, board, maximiser):
		"""
		This method will be implemented by the student as part of the lab. It
		is a recursive method that will search a game tree for an optimal move.
		It returns the score of the move (board) based on the minimax algorithm.

		:param board: The tictactoe game board
		:type board: TicTacToe
		:param maximiser: True if it's the maximiser's turn otherwise False
		:type maximiser: Boolean
		:return: Integer
		"""

		# *** NOT IMPLEMENTED YET!! ***

		if board.isGameOver():
			return self.scoreGame(board)

		children = board.remainingMoves
		scores = []

		for move in children:
			copyBoard = board.copy()
			if maximiser:
				copyBoard.makeMove(move, self.opponent)
			else:
				copyBoard.makeMove(move, self.letter)
			score = self.minimaxHelper(copyBoard, not maximiser)
			scores.append(score)

		if maximiser:
			return max(scores)

		return min(scores)


	def scoreGame(self, board):
		"""
		This method will be implemented by the student as part of the lab. This
		method will assign a score to the board.  It returns 10 if the player
		won, -10 if the opponent won, and 0 for all other conditions.

		:param board: The tictactoe game board
		:type board: TicTacToe
		:return: Integer
		"""

		# *** NOT IMPLEMENTED YET!! ***

		if board.getWinner() is None:
			return 0

		if board.getWinner().letter == self.letter:
			return 10

		if board.getWinner().letter == self.opponent:
			return -10

		return 0

class HUMANPlayer(Player) :
	"""
	This class represents a person playing tictactoe.
	"""

	def __init__(self, letter, playerType=HUMAN_AGENT):
		"""
		When creating a HUMANPlayer you must specify a letter, either 'X' or 'O'
		(both capitilised).  Do not specify the playerType.

		:param letter: The letter the player uses, can only be 'X' or 'O'
		:type letter: String
		:param playerType: HUMAN_AGENT
		:type playerType: Integer
		"""

		super().__init__(letter, playerType)

	def requestMove(self):
		"""
		This method ask the user to enter a move.  There's no input validation.
		The user should enter a number between 0 and 8 (inclusive).

		:return: Integer
		"""

		userInput = input("Player " + self.letter + ", enter a move (e.g. 0...8) : ")
		userInput = userInput.strip()

		if userInput == "quit":
			return None

		return int(userInput)

	def makeMove(self, board):
		"""
		This method allows a user, HUMAN, to enter his or her move

		:param board: The tictactoe game board
		:type board: TicTacToe
		"""

		moveLegal = False

		while not moveLegal:
			playerMove = self.requestMove()

			if playerMove is None :
				board.userQuit = True
				moveLegal = True
			else :
				moveLegal = board.makeMove(playerMove, self.letter)


class Tournament :
	"""
	This class performs a tournament between two tictactoe players. Four games
	are played where each player gets to go first twice twice.  By default the
	board is not drawn.  If a human is playing in the tournament, call
	enableHumanPlayer() to show the board.
	"""

	def __init__(self):
		self.humanPlaying = False

	def enableHumanPlayer(self) :
		"""
		This method enables board drawing, i.e., if called the board is
		drawn during the tournament.  This should only be used if one of the
		players is human.
		"""

		self.humanPlaying = True

	def start(self, player1, player2, games=1) :
		"""
		This method performs the tournament.  Four games are played.
		Each player gets to go first in 2 of the four games.

		:param player1: Player 1
		:type player1: Player, RLPlayer, MINIPlayer or HUMANPlayer
		:param player2: Player 2
		:type player2: Player, RLPlayer, MINIPlayer or HUMANPlayer
		:param games: The number of games to play
		:type games: Integer
		"""

		for _ in range(games):

			self.game(player1, player2)
			self.elo(player1, player2)

			if self.humanPlaying:
				if player1.winner:
					print(f'Winner: {player1.name}')
				elif player2.winner:
					print(f'Winner: {player2.name}')
				else:
					print(f'Draw')

	def game(self, p1, p2) :
		"""
		This method executes a single game of tictactoe between
		player1 and player2

		:param p1: Player 1
		:type p1: Player, RLPlayer, MINIPlayer or HUMANPlayer
		:param p2: Player 2
		:type p2: Player, RLPlayer, MINIPlayer or HUMANPlayer
		"""

		board = TicTacToe()
		board.setPlayers(p1, p2)

		if self.humanPlaying :
			board.drawBoard()

		while not board.isGameOver():

			player = board.next()
			player.makeMove(board)

			if self.humanPlaying :
				board.drawBoard()

		player = board.getWinner()

		if player:
			player.winner = True

	def elo(self, player1, player2) :
		"""
		This method updates each players rating according to the ELO rating
		system

		:param player1: Player 1
		:type player1: Player, RLPlayer, MINIPlayer or HUMANPlayer
		:param player2: Player 2
		:type player2: Player, RLPlayer, MINIPlayer or HUMANPlayer
		"""

		K = 30
		qa = 10**(player1.rating/400)
		qb = 10**(player2.rating/400)

		e1 = qa / (qa + qb)
		e2 = qb / (qa + qb)

		if player1.winner:
			r1 = player1.rating + K * (1 - e1)
			r2 = player2.rating + K * (0 - e2)
			player1.gamesW += 1
			player2.gamesL += 1
		elif player2.winner :
			r1 = player1.rating + K * (0 - e1)
			r2 = player2.rating + K * (1 - e2)
			player2.gamesW += 1
			player1.gamesL += 1
		else :
			r1 = player1.rating + K * (1 - e1)
			r2 = player2.rating + K * (1 - e2)
			player1.gamesD += 1
			player2.gamesD += 1

		player1.rating = r1
		player2.rating = r2

	def printStats(self, players) :
		"""
		This method prints the stats (number of games won, lost, drawn
		and rating) for player1 and player2

		:param players: List of Players
		"""

		for player in players :
			print(player.name  + " " + str(player.gamesW) +  "W " +
			str(player.gamesL) + "L " + str(player.gamesD) + "D " +
			str(round(player.rating,2)))


def playWithMinMaxPlayer():
    '''
    Call this method to start a match with The WithMinMaxPlayer.
    '''
    # Players
    player1 = createPlayer('X', MINIMAX_AGENT)
    player1.name = 'Amy'

    player2 = createPlayer('O', HUMAN_AGENT)
    player2.name = "Bob"

    # Create board
    board = TicTacToe()
    board.setPlayers(player1, player2)
    board.drawBoard()
    while not board.isGameOver():
        player = board.next()
        player.makeMove(board)
        board.drawBoard()
    winner = board.getWinner()
    if winner:
        print(f'Congratulations {winner.name}')


#老师的
# import TicTacToe as ttt
#
# def main():
# 	# Players
# 	rlAgent = ttt.createPlayer('X', ttt.RL_AGENT)
# 	rlAgent.name = 'Alice'
#
# 	partner = ttt.createPlayer('O', ttt.RANDOM_AGENT)
# 	partner.name = "Random"
#
# 	# Training Session
# 	rlAgent.initTraining(0.1, 1, 0.2)
# 	ttt.train(rlAgent, partner, 50000)
#
# 	# Evaluation
# 	rlAgent.setMode(ttt.PLAYING_MODE)
# 	tournament = ttt.Tournament()
# 	tournament.start(rlAgent, partner, 5)
# 	tournament.start(partner, rlAgent, 5)
# 	tournament.printStats([rlAgent, partner])
#
# main()
# # playWithMinMaxPlayer()


# 我同学的
def RLP_train(lr, dr, e):
    '''
    This method trains and validates the RLPlayer. The learning rate,
    Discount rate, Epsilon are set to 0.1, 1, 0.2 (non-optimal setting).
    Training Results:
        RL 7W 3L 0D 1230.04
        Random 3W 7L 0D 1169.96
    :return:
    '''
    #Players

    rlAgent = createPlayer('X', RL_AGENT)
    rlAgent.name = 'RL'

    partner = createPlayer('O', RANDOM_AGENT)
    partner.name = "Random"

    # Training Session
    rlAgent.initTraining(lr, dr, e)
    train(rlAgent, partner, 5000)

    # Evaluation
    rlAgent.setMode(PLAYING_MODE)
    tournament = Tournament()
    tournament.start(rlAgent, partner, 5)
    tournament.start(partner, rlAgent, 5)
    tournament.printStats([rlAgent, partner])
    return rlAgent.gamesW


if __name__ == "__main__":
    #playWithMinMaxPlayer()
    RLP_train(0.1, 1, 0.2)