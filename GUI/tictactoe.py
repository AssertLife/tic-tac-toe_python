from enum import Enum
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *


GRID_SIZE = 3
MARGIN_SIZE = 25
BOARD_SIZE = 270
HELP_SIZE = 115

class Shape:
	def __init__(self, color, txt):
		self._color = color
		self._txt = txt

#Java-like enums:3
class BoardShape(Enum):
	EMPTY = '#FFF'
	NOUGHTS = Shape('green', 'O')
	CROSSES = Shape('red', 'X')

class GameState(Enum):
	ERROR = -1
	NO_WIN = 0
	WIN = 1
	DRAW = 2

class TTTGame(QWidget):
	def __init__(self, parent = None):
		super(self.__class__, self).__init__(parent)

			#	Additional variables
		self._thelp = THelp(self)
		self._tboard = TBoard([TBoard.Player(BoardShape.NOUGHTS), TBoard.Player(BoardShape.CROSSES)]
									,self)
			#	SIGNALS & SLOTS
		self._tboard.game_state_sgnl.connect(self._thelp.on_games_state_)
		self._thelp._restart_b.clicked.connect(self._tboard.clear_board)

			#	INIT
		self.initUI()

	def initUI(self):
		print(QDesktopWidget().screenGeometry())
		self.setGeometry((QDesktopWidget().screenGeometry().width() / 2) - ((BOARD_SIZE + MARGIN_SIZE + HELP_SIZE) / 2),
						(QDesktopWidget().screenGeometry().height() / 2) - ((BOARD_SIZE + MARGIN_SIZE) / 2 ),
				BOARD_SIZE + MARGIN_SIZE + HELP_SIZE, BOARD_SIZE + MARGIN_SIZE)
		self.setWindowTitle(sys.argv[0])




		""" http://pyqt.sourceforge.net/Docs/PyQt4/qframe.html#details """




class THelp(QWidget):
	
	class THelpLabel(QLabel):
		def __init__(self, txt, rect, ss,
							parent):
			super(self.__class__, self).__init__(parent)

				#	INIT
			self.initUI(txt, rect , ss)

		def initUI(self, txt, rect, ss):
			self.setText(txt)
			self.setGeometry(rect)
			self.setStyleSheet(ss)


	def __init__(self, parent = None):
		super(self.__class__, self).__init__(parent)

			#	Additional variables
		self._parent = parent

		self._restart_b = QPushButton("Restart", self)
		self._restart_b.setGeometry(QRect(QPoint(MARGIN_SIZE - 10, 0), QSize(HELP_SIZE - MARGIN_SIZE, 25)))

		self._quit_b = QPushButton("Quit", self)
		self._quit_b.setGeometry(QRect(QPoint(MARGIN_SIZE - 10, MARGIN_SIZE + 5), QSize(HELP_SIZE - MARGIN_SIZE, 25)))

		self._game_state_lbl_vbl = THelp.THelpLabel(str(GameState.NO_WIN),
														QRect(QPoint(MARGIN_SIZE - 10, MARGIN_SIZE*3), QSize(HELP_SIZE, 25)),
														"""
														color: green;
														""",
														self)

			#ACTIONS
		self._quit_b.clicked.connect(QCoreApplication.instance().quit)


			#	INIT
		self.setGeometry(BOARD_SIZE + MARGIN_SIZE, MARGIN_SIZE, HELP_SIZE, BOARD_SIZE)

	#SIGNALS
			
	#SLOTS
	@pyqtSlot(GameState)
	def on_games_state_(self, game_state):
		self._game_state_lbl_vbl.setText(str(game_state))
		

class TBoard(QWidget):

	# Additional Classes
	class Player:
		def __init__(self, _board_shape):
			self._p_board_shape = _board_shape

	
	def __init__(self, players,
				parent = None,
					):
		super(self.__class__, self).__init__(parent)
			#	Additional variables
		self._board = [[CellShape(self, QPoint(column, row)) for row in range(0, GRID_SIZE)] for column in range(0, GRID_SIZE)]
		self._players = players
		self._player_index = 0
		self._round = 0
			#	INIT
		self.initUI()

			#	INIT
	def initUI(self):
		self.setGeometry(0, 0, BOARD_SIZE + MARGIN_SIZE, BOARD_SIZE + MARGIN_SIZE )



	def check_board_for_winner(self, position):
		player_next_move = self._players[self._player_index % len(self._players)]
		col=rw=diag=rdiag=0

		for i in range(0, GRID_SIZE):
			if player_next_move._p_board_shape == self._board[position.x()][i]._shape: rw += 1
			if player_next_move._p_board_shape == self._board[i][position.y()]._shape: col += 1
			if player_next_move._p_board_shape == self._board[i][i]._shape: diag += 1
			if player_next_move._p_board_shape == self._board[i][(GRID_SIZE-1) - i]._shape: rdiag += 1

		if rw == (GRID_SIZE) or \
			col == (GRID_SIZE) or \
			diag == (GRID_SIZE) or \
			rdiag == (GRID_SIZE):
			return GameState.WIN
		if self._round == (GRID_SIZE * GRID_SIZE):
			return GameState.DRAW
		return GameState.NO_WIN

	def insert_shape(self, clsp):
		if self._board[clsp._position.x()][clsp._position.y()]._shape != BoardShape.EMPTY or \
			self._round > (GRID_SIZE * GRID_SIZE):
			return GameState.ERROR
		self._board[clsp._position.x()][clsp._position.y()]._shape = self._players[self._player_index % len(self._players)]._p_board_shape
		self._round += 1

		return self.check_board_for_winner(clsp._position)

	#SIGNALS
	game_state_sgnl = pyqtSignal(GameState)

	#SLOTS
	@pyqtSlot()
	def clear_board(self):
		for column in range(0, GRID_SIZE):
			for row in range(0, GRID_SIZE):
				clsp = self._board[column][row]
				clsp.clear_clsp()
		self._player_index = 0
		self._round = 0
		self.game_state_sgnl.emit(GameState.NO_WIN)

class CellShape(QLabel):
	
	def __init__(self, parent,
				qp_position):
		super(self.__class__, self).__init__(parent)
			#	Additional variables
		self._parent = parent
		self._shape = BoardShape.EMPTY
		self._position = qp_position
			#	INIT
		self.initUI()
	
	def initUI(self):
		self.setGeometry((BOARD_SIZE / GRID_SIZE) * self._position.x() + MARGIN_SIZE, (BOARD_SIZE / GRID_SIZE) * self._position.y() + MARGIN_SIZE, (BOARD_SIZE / GRID_SIZE) - MARGIN_SIZE,  (BOARD_SIZE / GRID_SIZE) - MARGIN_SIZE)
		self.setStyleSheet("background-color: #CCC;")
		self.setAlignment(Qt.AlignCenter)
		self.setCursor(Qt.PointingHandCursor)
		self.setText("")

	def mousePressEvent(self, event):
		if self._shape != BoardShape.EMPTY or \
			self._parent._round == (GRID_SIZE * GRID_SIZE):
			return

		game_state = self._parent.insert_shape(self)
		self._parent.game_state_sgnl.emit(game_state)

		if game_state == GameState.WIN or \
			game_state == GameState.DRAW:
				self._parent._round = GRID_SIZE * GRID_SIZE

		self.draw_shape()
		self._parent._player_index += 1

	def draw_shape(self):
		self.setStyleSheet(str.format("background-color:{0};", self._shape.value._color))
		self.setText(self._shape.value._txt)

	def clear_clsp(self):
		self._shape = BoardShape.EMPTY
		self.initUI()

	#SIGNALS
	#SLOTS


		

def main():
	a =  QApplication(sys.argv)

	mw = TTTGame()
	mw.show()
	
	sys.exit(a.exec_())

main()