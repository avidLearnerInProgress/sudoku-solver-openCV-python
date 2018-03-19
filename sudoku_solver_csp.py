
def display_grid(grid, coords=False):
	"""
	Displays a 9x9 soduku grid in a nicely formatted way.
	Args:
		grid (str|dict|list): A string representing a Sudoku grid. Valid characters are digits from 1-9 and empty squares are
			specified by 0 or . only. Any other characters are ignored. A `ValueError` will be raised if the input does
			not specify exactly 81 valid grid positions.
			Can accept a dictionary where each key is the position on the board from A1 to I9.
			Can accept a list of strings or integers with empty squares represented by 0.
		coords (bool): Optionally prints the coordinate labels.
	Returns:
		str: Formatted depiction of a 9x9 soduku grid.
	"""
	if grid is None or grid is False:
		return None

	all_rows = 'ABCDEFGHI'
	all_cols = '123456789'
	null_chars = '0.'

	if type(grid) == str:
		grid = parse_puzzle(grid)
	elif type(grid) == list:
		grid = parse_puzzle(''.join([str(el) for el in grid]))

	width = max([3, max([len(grid[pos]) for pos in grid]) + 1])
	display = ''

	if coords:
		display += '   ' + ''.join([all_cols[i].center(width) for i in range(3)]) + '|'
		display += ''.join([all_cols[i].center(width) for i in range(3, 6)]) + '|'
		display += ''.join([all_cols[i].center(width) for i in range(6, 9)]) + '\n   '
		display += '--' + ''.join(['-' for x in range(width * 9)]) + '\n'

	row_counter = 0
	col_counter = 0
	for row in all_rows:
		if coords:
			display += all_rows[row_counter] + ' |'
		row_counter += 1
		for col in all_cols:
			col_counter += 1
			if grid[row + col] in null_chars:
				grid[row + col] = '.'

			display += ('%s' % grid[row + col]).center(width)
			if col_counter % 3 == 0 and col_counter % 9 != 0:
				display += '|'
			if col_counter % 9 == 0:
				display += '\n'
		if row_counter % 3 == 0 and row_counter != 9:
			if coords:
				display += '  |'
			display += '+'.join([''.join(['-' for x in range(width * 3)]) for y in range(3)]) + '\n'

	print(display)
	return display


def print_func(param):
	print(param)
	print(len(param))
	print("\n")

def sudoku_def():

	def cross_product(first, second): #Concatenates two strings first and second
			return [a + b for a in first for b in second]

	rows = 'ABCDEFGHI'
	cols = '123456789' #9x9

	mxn = cross_product(rows, cols) #m*n
	#print_func(mxn)

	#group by rows
	row_merge = [cross_product(row, cols) for row in rows]
	#print_func(row_merge)

	#group by columns
	col_merge = [cross_product(rows, col) for col in cols]
	#print_func(col_merge)

	#group by 3x3 boxes
	box_merge = [cross_product(row_box, col_box) for row_box in ['ABC', 'DEF', 'GHI'] for col_box in ['123', '456', '789']]
	#print(box_merge)


	all_merge = row_merge + col_merge + box_merge
	groups = {}

	#for each combination like A1, B1, C1 etc., group all the lists containing A1 together into a dictionary where key=A1 and val=list of lists containing A1
	
	'''
	_f = {}
	_dict = {}
	for pos in mxn:
		temp_list = []
		for unit in all_merge:
			if pos in unit:
				temp_list.append(unit)
		_f[pos] = temp_list
	_dict['ut'] = _f
	print_func(_dict['ut'])
	'''

	groups['units'] = {pos: [unit for unit in all_merge if pos in unit] for pos in mxn}
	#print_func(groups['units']['A1'])  #[['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'], ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1'], ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]

	#combine all the values grouped by units in previous step and remove the pos(i.e. A1) from the set
	'''
	_f = {}
	_dict = {}
	for pos in mxn:
		res = set(sum(groups['units'][pos], [])) - {pos}
		_dict[pos] = res

	_f['peers'] = _dict
	print_func(_f['peers']['A1'])
	'''

	groups['peers'] = {pos : set(sum(groups['units'][pos], [])) - {pos} for pos in mxn}
	#print_func(groups['peers']['A1']) #{'A3', 'A5', 'B2', 'A8', 'F1', 'D1', 'A2', 'A6', 'H1', 'B3', 'A4', 'I1', 'A7', 'G1', 'C2', 'C1', 'B1', 'C3', 'A9', 'E1'}

	return mxn, groups, all_merge



def parse_puzzle(puzzle, digits = '123456789', nulls = 'O.'):

	#Serialise the input into string
	#0/. denotes empty cell boards of sudoku
	#Ignore char not in digits or nulls
	flatten_puzzle = []
	for char in puzzle:
		if char in digits + nulls:
			if char in nulls:
				tmp = '.'
			else:
				tmp = char
			flatten_puzzle.append(tmp)
	
	#print(flatten_puzzle)

	if len(flatten_puzzle)!=81:
		raise ValueError('Input puzzle has %s positions specified! It must be 81'%len(flatten_puzzle))

	mxn, groups, all_merge = sudoku_def()

	#Convert list to dict using mxn as keys
	#for k,v in dict(zip(mxn, flatten_puzzle)):
	#	print(k+" : "+v)

	return dict(zip(mxn, flatten_puzzle))


def validate_sudoku(puzzle): #Checks if a completed Sudoku puzzle has a valid solution.

    if puzzle is None:
    	return False
    mxn, groups, all_merge = sudoku_def()
    full = [str(x) for x in range(1, 10)]  # Full set, 1-9 as strings
    # Checks if all units contain a full set
    return all([sorted([puzzle[cell] for cell in unit]) == full for unit in all_merge])

def solve_puzzle1(puzzle):
	
	digits = '123456789'

	mxn, groups, all_merge = sudoku_def()
	input_grid = parse_puzzle(puzzle)
	input_grid = {k: v for k, v in input_grid.items() if v != '.'}  #Map of each value from puzzle to its location in flattened_puzzle
	output_grid = {cell: digits for cell in mxn}  #Map of each cell in mxn to digits

	def confirm_value(grid, pos, val): #Confirm value by eliminating all other possibilities
		remaining_values = grid[pos].replace(val, '')  #Possibilities which can be eliminated
		for val in remaining_values:
			grid = eliminate(grid, pos, val)
		return grid

	def eliminate(grid, pos, val): #eliminate 'val' as possibility from all peers of 'pos'
		if grid is None:  #Exit if grid has already found a contradiction
			return None

		if val not in grid[pos]:  #If value is already eliminated, return board as it is
			return grid

		grid[pos] = grid[pos].replace(val, '')  #Remove possibility from given cell

		if len(grid[pos]) == 0:  #When there are no remaining possibility, we have made wrong decision
			return None
		elif len(grid[pos]) == 1:  #Digit is confirmed hence remove that value from all peers
			for peer in groups['peers'][pos]:
				grid = eliminate(grid, peer, grid[pos])  #Recursive, propagating the constraint
				if grid is None:  #Exit if grid has already found a contradiction
					return None

		#Number of remaining places that eliminated digit could possibly occupy
		for unit in groups['units'][pos]:
			#If there is only one possible position which has multiple possibilities, confirm digit
			possibilities = [p for p in unit if val in grid[p]]

			if len(possibilities) == 0:  #If there are no possible locations for the digit, we have made a mistake
				return None

			#If there is only one possible position and that still has multiple possibilities, confirm the digit
			elif len(possibilities) == 1 and len(grid[possibilities[0]]) > 1:
				if confirm_value(grid, possibilities[0], val) is None:
					return None

		return grid

	#First pass of constraint propagation
	for position, value in input_grid.items():
		output_grid = confirm_value(output_grid, position, value)

	if validate_sudoku(output_grid):  #If successful and validated return result
		return output_grid

	#Constraints
	#If there are no remaining possibilities for a cell, the board is invalid.
    #If there are no possible positions for a digit in a unit, the board is invalid.

	def guess_digit(grid): #Guess cell from fewest unconfirmed possibilities and porpagate constraints accordingly
		
		if grid is None:  #Exit if grid already compromised
			return None

		#Reached a valid solution, hence end
		if all([len(possibilities) == 1 for cell, possibilities in grid.items()]):
			return grid

		#Get the position and no of possibilities for cell with fewest remaining possibilities
		n, pos = min([(len(possibilities), cell) for cell, possibilities in grid.items() if len(possibilities) > 1])

		for val in grid[pos]:
			#Run the constraint propagation, but copy the grid as we will try many adn throw the bad ones away.
			#Recursively guess digits until its complete and there's a valid solution
			solution = guess_digit(confirm_value(grid.copy(), pos, val))
			if solution is not None:
				return solution

	output_grid = guess_digit(output_grid)
	return output_grid

if __name__ == '__main__':

	# Easy Sudoku Puzzle
	puzzle1 = """
	1  .  5 | .  7  . | 4  .  .
	.  8  . | 2  .  . | .  .  .
	7  2  4 | .  .  1 | .  .  6
	---------+---------+---------
	.  .  . | 3  2  5 | .  .  .
	2  3  7 | .  .  . | 1  4  5
	6  .  . | 4  1  7 | .  .  .
	---------+---------+---------
	8  .  . | 1  .  . | 6  2  4
	.  .  . | .  .  3 | .  5  .
	.  .  1 | .  4  . | 3  .  9
	"""

	# Arto Inkala's 2012 Puzzle
	puzzle2 = """
	8  .  . | .  .  . | .  .  .
	.  .  3 | 6  .  . | .  .  .
	.  7  . | .  9  . | 2  .  .
	---------+---------+---------
	.  5  . | .  .  7 | .  .  .
	.  .  . | .  4  5 | 7  .  .
	.  .  . | 1  .  . | .  3  .
	---------+---------+---------
	.  .  1 | .  .  . | .  6  8
	.  .  8 | 5  .  . | .  1  .
	.  9  . | .  .  . | 4  .  .
	"""
	
	print("Input puzzle: (Arto Inkalas: Hardest Puzzle)\n")
	display_grid(puzzle2)

	print("\n Output Results:\n")
	display_grid(solve_puzzle1(puzzle2))