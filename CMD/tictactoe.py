# tic-tac-toe without general user interafce

import random
import sys
from enum import Enum

#PLAYER STATE
WAITING = 0
OTHER_PLAYER = 1

#GRID
LENGTH = WIDTH = 3

#BOARD SHAPES
class BoardShapes(Enum):
	EMPTY = 0
	NOUGHTS = 1
	CROSSES = 2
#GAME_STATE
class GameState(Enum):
	OTHER_PLAYING = -1
	NO_WIN = 0
	SUCCESS_WON = 1
	ALREADY_DROWN = 2
	DRAW = 3
	GAME_OVER = 4


class Board:

	def __init__(self, player1, player2):
		self._last_game_state = GameState.NO_WIN
		self._round = 0
		self._board = [[BoardShapes.EMPTY for x in range(WIDTH)] for y in range(LENGTH)]

		self._player1 = player1
		self._player2 = player2

	def clean_board(self):
		for next_row in self._board:
			for next_column in next_row:
				self._board[next_row][next_column] = BoardShapes.EMPTY

	def get_other_player(self, current):
		if current == self._player1:
			return self._player2
		return self._player1

	def check_board_for_winner(self, player_next_move, position):

		col=rw=diag=rdiag=0
		column, row = position

		#rows
		for i in range(0, LENGTH):
			if player_next_move._p_shape == self._board[column][i]: rw += 1
			if player_next_move._p_shape == self._board[i][row]: col += 1
			if player_next_move._p_shape == self._board[i][i]: diag += 1
			if player_next_move._p_shape == self._board[i][(LENGTH-1)-i]: rdiag += 1

		if rw == (LENGTH) or \
			col == (LENGTH) or \
			diag == (LENGTH) or \
			rdiag == (LENGTH):
			self._last_game_state = GameState.GAME_OVER
			return GameState.SUCCESS_WON

		if self._round == LENGTH * WIDTH:
			return GameState.DRAW
		return GameState.NO_WIN

	def draw_shape(self, player, position):
		if player._state == OTHER_PLAYER:
			return OTHER_PLAYING

		i_other_player = self.get_other_player(player)

		print("other STATE:", i_other_player._state)

		if i_other_player._state == OTHER_PLAYER or \
			(player._state == WAITING and i_other_player._state == WAITING):
			column, row = position

			if self._board[column][row] == BoardShapes.EMPTY:
				self._round += 1
				#///
				self._board[column][row] = player._p_shape
				#///

			else:
				if self._round == LENGTH * WIDTH or \
					self._last_game_state == GameState.GAME_OVER:
					return GameState.GAME_OVER
				return GameState.ALREADY_DROWN
			return self.check_board_for_winner(player, position)
		return GameState.NO_WIN

	class Player:
		def __init__(self, p_shape):
			self._p_shape = p_shape
			self._state = WAITING
		def __eq__(self, other):
			if isinstance(other, self.__class__):
				return self._p_shape == other._p_shape
			return False
		def __ne__(self, other):
			if isinstance(other, self.__class__):
				return self._p_shape != other._p_shape
			return False


def main():
	player1 = Board.Player(BoardShapes.NOUGHTS)
	player2 = Board.Player(BoardShapes.CROSSES)

	b = Board(player1, player2)

	lplayer = [player1, player2]
	count = 0
	while raw_input("->Continue? (y/n)") == "y":
		player_index = count % 2
		current_player = lplayer[player_index]

		position = (random.randint(0, 2), random.randint(0, 2))

		ret = b.draw_shape(current_player, position)

		if ret == GameState.OTHER_PLAYING:
			print(str.format("[{0}] The other player is making a move, hold on.". sys.argv[0]))
			count -= 1
		elif ret == GameState.NO_WIN:
			print(str.format("[{0}] The shape is drawn but {1} haven't won yet.", sys.argv[0], current_player._p_shape))
		elif ret == GameState.SUCCESS_WON:
			print(str.format("[{0}] Shape {1} has won!", sys.argv[0], current_player._p_shape))
		elif ret == GameState.ALREADY_DROWN:
			print(str.format("[{0}] This position is already drawn, please try another one.", sys.argv[0]))
		elif ret == GameState.DRAW:
			print(str.format("[{0}] It's a draw!", sys.argv[0]))
		elif ret == GameState.GAME_OVER:
			print(str.format("[{0}] The game is over.", sys.argv[0]))

		count += 1

	print(b._board)

	

main()
			