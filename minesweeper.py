from random import randrange

MINE_FOUND = 'X'
UNDISCOVERED = ' '
MINE = 1
EMPTY = 0

class Board(object):

	def __init__(self, height, width, num_mines):
		if num_mines <= height * width and height < 100 and width < 100:
			self.height = height
			self.width = width
			self.num_mines = num_mines
			self.initialize_mines()
			self.user_board = [[UNDISCOVERED for row in range(self.height)] for col in range(self.width)]
			self.remaining_cells = self.height * self.width - self.num_mines
		else:
			raise ValueError()

	def initialize_mines(self):
		self.mines = [[EMPTY for row in range(self.height)] for col in range(self.width)]
		remaining_mines = self.num_mines
		while remaining_mines > 0:
			col = randrange(0, self.width)
			row = randrange(0, self.height)
			if self.mines[col][row] != MINE:
				self.mines[col][row] = MINE
				remaining_mines -= 1

	def discover_cell(self, col, row):
		if self.mines[col][row] == MINE:
			self.copy_mines_to_user_board()
			return True

		total_mines = 0
		undiscovered_cells = []
		for i in range(-1, 2):
			for j in range(-1, 2):
				if col + i >= 0 and col + i < self.width and row + j >= 0 and row + j < self.height:
					if self.mines[col + i][row + j] == MINE:
						total_mines += 1
					if (i != 0 or j != 0) and self.user_board[col + i][row + j] == UNDISCOVERED:
						undiscovered_cells.append((col + i, row + j))

		self.user_board[col][row] = total_mines
		self.remaining_cells -= 1

		if total_mines == 0:
			for x, y in undiscovered_cells:
				if self.user_board[x][y] == UNDISCOVERED:
					self.discover_cell(x, y)

		return False

	def copy_mines_to_user_board(self):
		for col in range(self.width):
			for row in range(self.height):
				if self.mines[col][row] == MINE:
					self.user_board[col][row] = MINE_FOUND

	def play_user(self):
		while self.remaining_cells > 0:
			self.clear_terminal()
			self.print_board()
			(col, row) = self.ask_input()
			if self.discover_cell(col, row):
				self.end_game("BOOOOM! You loose...")
				return False
		self.end_game("Phew! You are safe. You win!")
		return True

	def end_game(self, msg):
		self.clear_terminal()
		self.print_board()
		print msg

	def ask_input(self):
		while True:
			(col, row) = (0, 0)
			while row < 1 or row > self.height:
				try:
					row = int(raw_input("Select row (between %d and %d): " % (1, self.height)))
				except ValueError:
					print "Please, input a number."
			while col < 1 or col > self.width:
				try:
					col = int(raw_input("Select column (between %d and %d): " % (1, self.width)))
				except ValueError:
					print "Please, input a number."

			if self.user_board[col - 1][row - 1] == UNDISCOVERED:
				break
			else:
				print "That cell has already been discovered."
		return (col - 1, row - 1)	

	def print_board(self):
		# print indexes of the board and upper border of the board
		if self.width > 9:
			print "\t  " + "   ".join([str(row + 1) for row in range(10)]),
			print " " + "  ".join([str(row + 1) for row in range(10, self.width)]) + "\n"
		else:
			print "\t  " + "   ".join([str(row + 1) for row in range(self.width)]) + "\n"
		print "\t|" + "".join([" - |" for row in range(self.width)])

		# print row, separator between rows and bottom border of the board
		for row in range(self.height):
			print str(row + 1) + "\t| " + " | ".join([str(self.user_board[col][row]) for col in range(self.width)]) + " |"
			print "\t|" + "".join([" - |" for row in range(self.width)])

		# print a blank line just for cleanliness
		print

	def clear_terminal(self):
		for i in range(50):
			print
