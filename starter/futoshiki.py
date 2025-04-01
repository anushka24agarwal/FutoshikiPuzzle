"""
Each futoshiki board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8

Empty values in the board are represented by 0

An * after the letter indicates the inequality between the row represented
by the letter and the next row.
e.g. my_board['A*1'] = '<' 
means the value at A1 must be less than the value
at B1

Similarly, an * after the number indicates the inequality between the
column represented by the number and the next column.
e.g. my_board['A1*'] = '>' 
means the value at A1 is greater than the value
at A2

Empty inequalities in the board are represented as '-'

"""
import sys

#======================================================================#
#*#*#*# Optional: Import any allowed libraries you may need here #*#*#*#
#======================================================================#

import numpy as np

import time

#=================================#
#*#*#*# Your code ends here #*#*#*#
#=================================#

ROW = "ABCDEFGHI"
COL = "123456789"

class Board:
	'''
	Class to represent a board, including its configuration, dimensions, and domains
	'''
	
	def get_board_dim(self, str_len):
		'''
		Returns the side length of the board given a particular input string length
		'''
		d = 4 + 12 * str_len
		n = (2+np.sqrt(4+12*str_len))/6
		if(int(n) != n):
			raise Exception("Invalid configuration string length")
		
		return int(n)
		
	def get_config_str(self):
		'''
		Returns the configuration string
		'''
		result = ""
		config = self.get_config()
		for row in ROW:
			for col in COL:
				# Append the number in the current cell
				result += str(config.get(row + col, ""))
				# Append any symbols in the corresponding * cell
				result += config.get(row + col + '*', "")
			for col in COL:
				result += config.get(row + '*'+ col, "")
		self.config_str = result
		return self.config_str
		
	def get_config(self):
		'''
		Returns the configuration dictionary
		'''
		return self.config
		
	def get_variables(self):
		'''
		Returns a list containing the names of all variables in the futoshiki board
		'''
		variables = []
		for i in range(0, self.n):
			for j in range(0, self.n):
				variables.append(ROW[i] + COL[j])
		return variables
	
	def convert_string_to_dict(self, config_string):
		'''
		Parses an input configuration string, retuns a dictionary to represent the board configuration
		as described above
		'''
		config_dict = {}
		
		for i in range(0, self.n):
			for j in range(0, self.n):
				cur = config_string[0]
				config_string = config_string[1:]
				
				config_dict[ROW[i] + COL[j]] = int(cur)
				
				if(j != self.n - 1):
					cur = config_string[0]
					config_string = config_string[1:]
					config_dict[ROW[i] + COL[j] + '*'] = cur
					
			if(i != self.n - 1):
				for j in range(0, self.n):
					cur = config_string[0]
					config_string = config_string[1:]
					config_dict[ROW[i] + '*' + COL[j]] = cur
					
		return config_dict
		
	def print_board(self):
		'''
		Prints the current board to stdout
		'''
		config_dict = self.config
		for i in range(0, self.n):
			for j in range(0, self.n):
				cur = config_dict[ROW[i] + COL[j]]
				if(cur == 0):
					print('_', end=' ')
				else:
					print(str(cur), end=' ')
				
				if(j != self.n - 1):
					cur = config_dict[ROW[i] + COL[j] + '*']
					if(cur == '-'):
						print(' ', end=' ')
					else:
						print(cur, end=' ')
			print('')
			if(i != self.n - 1):
				for j in range(0, self.n):
					cur = config_dict[ROW[i] + '*' + COL[j]]
					if(cur == '-'):
						print(' ', end='   ')
					else:
						print(cur, end='   ')
			print('')
	
	def __init__(self, config_string):
		'''
		Initialising the board
		'''
		self.config_str = config_string
		self.n = self.get_board_dim(len(config_string))
		if(self.n > 9):
			raise Exception("Board too big")
			
		self.config = self.convert_string_to_dict(config_string)
		self.domains = self.reset_domains()
		
		self.forward_checking(self.get_variables())
		
		
	def __str__(self):
		'''
		Returns a string displaying the board in a visual format. Same format as print_board()
		'''
		output = ''
		config_dict = self.config
		for i in range(0, self.n):
			for j in range(0, self.n):
				cur = config_dict[ROW[i] + COL[j]]
				if(cur == 0):
					output += '_ '
				else:
					output += str(cur)+ ' '
				
				if(j != self.n - 1):
					cur = config_dict[ROW[i] + COL[j] + '*']
					if(cur == '-'):
						output += '  '
					else:
						output += cur + ' '
			output += '\n'
			if(i != self.n - 1):
				for j in range(0, self.n):
					cur = config_dict[ROW[i] + '*' + COL[j]]
					if(cur == '-'):
						output += '    '
					else:
						output += cur + '   '
			output += '\n'
		return output
		
	def reset_domains(self):
		'''
		Resets the domains of the board assuming no enforcement of constraints
		'''
		domains = {}
		variables = self.get_variables()
		for var in variables:
			if(self.config[var] == 0):
				domains[var] = [i for i in range(1,self.n+1)]
			else:
				domains[var] = [self.config[var]]
				
		self.domains = domains
				
		return domains 
		


		#======================================================================#
		#*#*#*# TODO: Write your implementation of forward checking here #*#*#*#
		#======================================================================#

			
	def forward_checking(self, reassigned_variables):
		"""Apply forward checking to update domains based on constraints."""

		
		current_domain_copy = {var:self.domains[var][:] for var in self.get_variables()}
		

		for var in reassigned_variables:
			value = self.config[var]
			row, col = var[0], var[1]
			
			#if the value is not 0:
				#check for row constraint and prune
				#check for column constraint and prune
				
			#if the value is 0
				#continue
			
			if(value!=0):
				#for value in domain of other vars in row, prune the domain 
				#this time only check for duplicates
				for i in range(self.n):
					other_var = ROW[ROW.index(var[0])]+COL[i]
					if other_var != var:
						if value in self.domains[other_var]:
							self.domains[other_var].remove(value)

				#for value in domain of other vars in col
				#this time only check for duplicates

				for i in range(self.n):
					other_var = ROW[i]+COL[COL.index(var[1])]
					if other_var != var:
						if value in self.domains[other_var]:
							self.domains[other_var].remove(value)
			else:
				continue

		# Apply inequalities
		if(value!=0):
			
			if not self.apply_inequality_constraints(var, value):
				board.domains= current_domain_copy
			else:
				return True
				
			#if inequality returns false, return false 

		#return True 
			
		#=================================#
		#*#*#*# Your code ends here #*#*#*#
		#=================================#
		
	#=================================================================================#
	#*#*#*# Optional: Write any other functions you may need in the Board Class #*#*#*#
	#=================================================================================#

	def apply_inequality_constraints(self, var, value):
		"""Adjust domains based on inequality constraints."""

		row, col = var[0], var[1]

		#checking for all the inequalities: left, right, up and down 
		
		# Handle row inequalities
		# right neighbour
		if int(col) <= self.n-1:
			
			right_neighbor = row + COL[int(col)]
			constraint = self.config.get(var + '*', '-')
			if constraint == '<':
				if len(self.domains[right_neighbor])!= 1:
					self.domains[right_neighbor] = [v for v in self.domains[right_neighbor] if v > value]
				else:
					if self.config.get(row + str(int(col) +1)) != 0 and value >= self.config.get(row + str(int(col) + 1)):  # Check if right neighbor is assigned
						return False
			elif constraint == '>':
				if len(self.domains[right_neighbor])!=1:
					self.domains[right_neighbor] = [v for v in self.domains[right_neighbor] if v < value]
				else:
					if self.config.get(row + str(int(col) + 1)) != 0 and value <= self.config.get(row + str(int(col) + 1)):  # Check if right neighbor is assigned
						return False
			
			if(len(self.domains[right_neighbor]) == 0):
				
				return False
			

		#left neighbour
		if int(col) > 1:
			left_neighbor = row + COL[int(col)-2]
			constraint = self.config.get(left_neighbor + '*', '-')
			
			if constraint == '<':
				if not len(self.domains[left_neighbor]) == 1:
					self.domains[left_neighbor] = [v for v in self.domains[left_neighbor] if v < value]
				else:
					if self.config.get(row + str(int(col)-1)) != 0 and value <= self.config.get(row + str(int(col) - 1)):  # Check if right neighbor is assigned
						return False
			elif constraint == '>':
				if len(self.domains[left_neighbor])!=1:
					self.domains[left_neighbor] = [v for v in self.domains[left_neighbor] if v > value]
				else:
					if self.config.get(row + str(int(col) - 1)) != 0 and value >= self.config.get(row + str(int(col) - 1)):  # Check if right neighbor is assigned
						return False
			
			if(len(self.domains[left_neighbor]) == 0):
				return False

		# Handle column inequalities
		#below neighbor
		if row < ROW[self.n-1]:
			below_neighbor = ROW[ROW.index(row) + 1] + col
			constraint = self.config.get(row + '*' + col, '-')
			if constraint == '<':
				if len(self.domains[below_neighbor])!=1:
					self.domains[below_neighbor] = [v for v in self.domains[below_neighbor] if v > value]
				else:
					if self.config.get(ROW[ROW.index(row) + 1] + col) != 0 and value >= self.config.get(ROW[ROW.index(row) + 1] + col):  # Check if right neighbor is assigned
						return False
			elif constraint == '>':
				if len(self.domains[below_neighbor])!=1:
					self.domains[below_neighbor] = [v for v in self.domains[below_neighbor] if v < value]
				else:
					if self.config.get(ROW[ROW.index(row) + 1] + col) != 0 and value <= self.config.get(ROW[ROW.index(row) + 1] + col):  # Check if right neighbor is assigned
						return False
			
			if(len(self.domains[below_neighbor]) == 0):
				return False

		#above neighbor
		if row > ROW[0]:
			above_neighbor = ROW[ROW.index(row) - 1] + col
			constraint = self.config.get(ROW[ROW.index(row) - 1] + '*' + col, '-')
			if constraint == '<':
				if len(self.domains[above_neighbor])!=1:
					self.domains[above_neighbor] = [v for v in self.domains[above_neighbor] if v < value]
				else:
					if self.config.get(ROW[ROW.index(row) - 1] + col) != 0 and value <= self.config.get(ROW[ROW.index(row) - 1] + col):  # Check if right neighbor is assigned
						return False
			elif constraint == '>':
				if len(self.domains[above_neighbor])!=1:
					self.domains[above_neighbor] = [v for v in self.domains[above_neighbor] if v > value]
				else:
					if self.config.get(ROW[ROW.index(row) - 1] + col) != 0 and value >= self.config.get(ROW[ROW.index(row) - 1] + col):  # Check if right neighbor is assigned
						return False
			
			if(len(self.domains[above_neighbor]) == 0):
				return False
			
		return True

		
	#=================================#
	#*#*#*# Your code ends here #*#*#*#
	#=================================#

#================================================================================#
#*#*#*# Optional: You may write helper functions in this space if required #*#*#*#
#================================================================================#  

def is_solved(board):
	"""Check if the board is solved."""
	return all(value != 0 for value in board.config.values())

def select_unassigned_variable(board):
	"""Select an unassigned variable."""
	unassigned_vars = [var for var, value in board.config.items() if value == 0]
	# Select variable with the smallest domain
	return min(unassigned_vars, key=lambda var: len(board.domains[var]), default=None) 
	

#=================================#
#*#*#*# Your code ends here #*#*#*#
#=================================#

def backtracking(board):
	"""Solve the board using backtracking."""

	if is_solved(board):
		return board
	
	#create a copy of the current domain  

	variable = select_unassigned_variable(board)
	row, col = variable[0], variable[1]
	
	# current_domain_copy = {var:board.domains[var][:] for var in board.get_variables()}
	# print("current domain copy in BT of",variable, current_domain_copy)
	# current_domain_copy = {var:board.domains[var][:] for var in board.get_variables()}
	original_domains = {var: board.domains[var][:] for var in board.get_variables()}
	for value in original_domains[variable]:
		board.config[variable]=value
		# Create a copy of the domains for this iteration
		board.domains = {var: original_domains[var][:] for var in board.get_variables()}
		if is_consistent(board, row, col, value):
			if board.forward_checking([variable]):
				result = backtracking(board)  # Recursive call
				if result:
					return result  # Return if a solution is found

		# If we reach here, we need to backtrack
		board.config[variable] = 0  # Unassign the variable


	return False

def is_consistent(board, row, col, value):
	# Check for row and column constraints
	for i in range(board.n):
		if (COL[i] != col):
			if board.config[row + COL[i]]==value:
				return False
		if (ROW[i] != row):
			if board.config[ROW[i] + col]==value:
				return False
	return True
#     #==========================================================#
# 	#*#*#*# TODO: Write your backtracking algorithm here #*#*#*#
# 	#==========================================================#

#     #=================================#
# 	#*#*#*# Your code ends here #*#*#*#
# 	#=================================#
	
def solve_board(board):
	'''
	Runs the backtrack helper and times its performance.
	Returns the solved board and the runtime
	'''
	start_time = time.time()  # Start timer

	solved_board = backtracking(board)  # Call the backtracking algorithm

	end_time = time.time()  # End timer
	runtime = end_time - start_time  # Calculate runtime

	return solved_board, runtime  # Return the solved board and runtime
	#================================================================#
	#*#*#*# TODO: Call your backtracking algorithm and time it #*#*#*#
	#================================================================#
	
	#return None, -1 # Replace with return values
	#=================================#
	#*#*#*# Your code ends here #*#*#*#
	#=================================#

def print_stats(runtimes):
	'''
	Prints a statistical summary of the runtimes of all the boards
	'''
	min = 100000000000
	max = 0
	sum = 0
	n = len(runtimes)

	for runtime in runtimes:
		sum += runtime
		if(runtime < min):
			min = runtime
		if(runtime > max):
			max = runtime

	mean = sum/n

	sum_diff_squared = 0

	for runtime in runtimes:
		sum_diff_squared += (runtime-mean)*(runtime-mean)

	std_dev = np.sqrt(sum_diff_squared/n)

	print("\nRuntime Statistics:")
	print("Number of Boards = {:d}".format(n))
	print("Min Runtime = {:.8f}".format(min))
	print("Max Runtime = {:.8f}".format(max))
	print("Mean Runtime = {:.8f}".format(mean))
	print("Standard Deviation of Runtime = {:.8f}".format(std_dev))
	print("Total Runtime = {:.8f}".format(sum))


if __name__ == '__main__':
	if len(sys.argv) > 1:

		# Running futoshiki solver with one board $python3 futoshiki.py <input_string>.
		print("\nInput String:")
		print(sys.argv[1])
		
		print("\nFormatted Input Board:")
		board = Board(sys.argv[1])
		board.print_board()
		
		solved_board, runtime = solve_board(board)
		
		print("\nSolved String:")
		print(solved_board.get_config_str())
		
		print("\nFormatted Solved Board:")
		solved_board.print_board()
		
		print_stats([runtime])

		# Write board to file
		out_filename = 'output.txt'
		outfile = open(out_filename, "w")
		outfile.write(solved_board.get_config_str())
		outfile.write('\n')
		outfile.close()

	else:
		# Running futoshiki solver for boards in futoshiki_start.txt $python3 futoshiki.py

		#  Read boards from source.
		src_filename = 'futoshiki_start.txt'
		try:
			srcfile = open(src_filename, "r")
			futoshiki_list = srcfile.read()
			srcfile.close()
		except:
			print("Error reading the sudoku file %s" % src_filename)
			exit()

		# Setup output file
		out_filename = 'output.txt'
		outfile = open(out_filename, "w")
		
		runtimes = []

		# Solve each board using backtracking
		for line in futoshiki_list.split("\n"):
			
			print("\nInput String:")
			print(line)
			
			print("\nFormatted Input Board:")
			board = Board(line)
			board.print_board()
			
			solved_board, runtime = solve_board(board)
			runtimes.append(runtime)
			
			print("\nSolved String:")
			print(solved_board.get_config_str())
			
			print("\nFormatted Solved Board:")
			solved_board.print_board()

			# Write board to file
			outfile.write(solved_board.get_config_str())
			outfile.write('\n')

		# Timing Runs
		print_stats(runtimes)
		
		outfile.close()
		print("\nFinished all boards in file.\n")
