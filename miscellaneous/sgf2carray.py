# This script requires the gomill library: https://pypi.org/project/gomill/
from gomill import sgf
from gomill import sgf_moves

# Change filename to use a different SGF file as input
FILENAME = '24-gokifu-19331016-Honinbo_Shusai-Go_Seigen_edited.sgf'
WRITE_FILENAME = 'carray.txt'

# The program will only save the game state in a C array every STEP_SIZE moves (to make the array smaller)
STEP_SIZE = 6

file = open(FILENAME, 'r')
data = file.read()
g = sgf.Sgf_game.from_string(data)
# print g.get_size()
# print g.serialise()

(board, moves) = sgf_moves.get_setup_and_moves(g)
print moves

board_size = g.get_size()
array_size = 0

game_carray = "{\n\n"

# Play game move-by-move and take a snapshot as a C array every STEP_SIZE
ii = start = 0
for i in range(len(moves)):
	move = moves[i]
	board.play(move[1][0], move[1][1], move[0])
	
	if i == ii or i == len(moves) - 1:
		array_size += 1
		
		board_carray = "{\n{"
		curr_row = 0
		for point in board.board_points:
			if point[0] == curr_row + 1:
				curr_row = point[0]
				board_carray += "},\n{"
			piece = board.get(point[0], point[1])
			if piece is None:
				piece = 'n'
			if point[1] != 0:
				board_carray += " ,"
			board_carray += "'{}'".format(piece)

		board_carray += "}\n}"
		
		if i != start:
			game_carray += ",\n\n"
			
		game_carray += board_carray
		
		ii = min(ii + STEP_SIZE, len(moves) - 1)
game_carray += "\n\n};"

# Generate code to assign the array of game states to a variable
game_carray = "char game[{states}][{size}][{size}] = \n".format(size=board_size, states=array_size) + game_carray

# Print results to the screen for debugging
print game_carray
print array_size

# Write results to a file
write_file = open(WRITE_FILENAME, 'w')
write_file.write(game_carray)
write_file.close()
