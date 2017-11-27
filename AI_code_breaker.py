# source of algorithm: https://lirias.kuleuven.be/bitstream/123456789/164803/1/kbi_0806.pdf

import sys
import numpy
import tkinter
import random

P_CROSS_OVER = 0.5
P_INVERT = 0.02
P_MUTATE = 0.03
MAX_GEN = 100
MAX_POP = 10


def GA(n_peg, n_col, guess, response):


# fotness fxn that's inversely proportional to the difference between the solution and the value a decoded chromosome represents


	def cross_over(g1,g2):
		if random.random() >= P_CROSS_OVER:
			cross_loc = random.randint(1, n_peg-1)
			new_g = g1[0:cross_loc] + g2[cross_loc:]


	
	h = 1
	# E = set of eligible codes at iteration i
	E_i = []

	# initialize the population
	population = [[random.randint(1, n_col) for i in range(n_peg)] for j in range(MAX_POP)]
	
	
	while(h <= MAX_GEN and len(E_i) <= MAX_POP):
		# generate new pop with crossover, mutation, inversion, permutation
		#child = crossover()
		# calc fitness

		# add eligible combos to E if not there yet
		h += 1

	#play something from E 





def AI_play(code, n_col, n_peg, response):

	# if this is the first guess, generate randomly
	if response == NULL:
		# assign an interger to each possible color
		colors = range(1,n_col)
		# play initial random guess
		curr_guess = numpy.random.choice(colors, n_pegs)

	else:
		X_i = response[0]
		Y_i = response[1]
		if(X_i != n_peg):
			print("not perfect")
			guess = GA(n_peg, n_col, curr_guess, response)




def person_play(guess, code):
	# X_i = exact number of matches in iteration i (red pegs)
	X_i = 0
	# Y_i = number of partial matches in iteration i (white pegs)
	Y_i = 0
	# get info from GUI about response

	#simulate response from person
	j = 0
	for i in range(length(code)):
		if guess[i] == code[i]:
			X_i += 1
		else if guess[i] in code and j == 0:
			Y_i += 1
			j += 1
		else:
			pass

	return [X_i, Y_i]




# method that controls the alternating turns
def play(n_col, n_peg, n_turns,code):
	
	turn = 1
	response = NULL
	while(turn <= n_turns):

		if turn == 1:
			#code = start_game()
			colors = range(1,n_col)
			code = numpy.random.choice(colors, n_pegs)
			print(code)

		elif turn % 2 == 0:
			guess = AI_play(code, n_col, n_peg, response)
			# show the guess on the GUI

		else:
			response = person_play(guess, code)
			# show the response on the GUI

		turn += 1


def main():

	# DEFINITIONS
	# num_colors = the number of color options
	num_colors = int(sys.argv[1])
	# the number of pegs that can be used in a code
	num_pegs = int(sys.argv[2])








if __name__ == "__main__":
	main()
