# source of algorithm: https://lirias.kuleuven.be/bitstream/123456789/164803/1/kbi_0806.pdf

import sys
import numpy
import tkinter
import random

P_CROSS_OVER = 0.5
P_INVERT = 0.03
P_MUTATE = 0.03
P_PERMUTE = 0.03
MAX_GEN = 100
MAX_POP = 60
REQ_FIT = 0.6


def remove_dups(seq):
   # Not order preserving
   keys = {}
   for e in seq:
       keys[e] = 1
   return keys.keys()


def GA(n_peg, n_col, guess, response):


# fitness fxn that's inversely proportional to the difference between the solution and the value a decoded chromosome represents


	def cross_over(g1,g2):
		#if random.random() < P_CROSS_OVER:
		cross_loc = random.randint(1, n_peg-1)
		new_g1 = g1[0:cross_loc] + g2[cross_loc:]
		new_g2 = g2[0:cross_loc] + g1[cross_loc:]
		return([new_g1, new_g2])


	def mutate(g1, n_peg, n_col):
		if(random.random() < P_MUTATE):
			loc = random.randint(0, n_peg-1)
			col = random.randint(1, n_col)
			g1[loc] = col
		return(g1)

	def get_fitness(g1, g2, response):
		X_i = response[1]
		Y_i = response[2]
		Xi_g2 = 0
		for i in range(len(g1)):
			if(g1[i] == g2[i]):
				Xi_g2 += 1
			
		
		fitness_g2 = X_i + 1/2 * Y_i
		return(fitness_g2)




	# initialize the population and remove any duplicates
	population = [[random.randint(1, n_col) for i in range(n_peg)] for j in range(MAX_POP)]
	
	# h = iteration number
	h = 1
	# E = set of eligible/elite codes at iteration h
	E_h = []
	
	while(h <= MAX_GEN and len(E_h) <= MAX_POP):


		# first evaluate the population and take some of the best + some random
		fitness = []
		for indiv in population:
			fitness.append(get_fitness(guess, indiv, response))

		# the new generation will contain some of the best indivs in this gen + randoms,
		# crossed over offspring of some,
		# mutations of some
		# use fitness values as probabilities to choose best indivs to keep same
		new_gen = numpy.random.choice(population, size = MAX_POP*(1-P_CROSS_OVER), replace=False, p = fitness)

		# select parents from previous gen using fitness values as probabilities
		parents = numpy.random.choice(population, size= MAX_POP*P_CROSS_OVER-10, replace=False, p = fitness)
		# add some random indiv to parental pool promote genetic diversity
		while len(parents) < MAX_POP*P_CROSS_OVER:
			parents.append([random.randint(1, n_col) for i in range(n_peg)])

		random.shuffle(parents)

		children = []
		i = 0
		while i < len(parents):
			child = cross_over(parents[i], parents[i+1])
			if random.random() <= CROSSOVER_THEN_MUTATION_PROBABILITY:
				child = [mutate(child[1]), mutate(child[2])]
			children.extend(child)
			i += 2

		# add the kids to the new population
		new_gen.extend(children)

		#get fitness of the elements in this new gen
		fitness = []
		for indiv in new_gen:
			fitness.append(get_fitness(guess,indiv, response))

		# add eligible codes to E_h e.g. codes with fitness above a required value
		for f in range(len(fitness)):
			if fitness[f] >= REQ_FIT:
				E_h.append(new_gen[f])

		# remove dups in eligibles
		E_h = remove_dups(E_h)

		population = E_h
		# fill remaining spot with random and remove duplicates again
		while len(population) < MAX_POP:
			population.append([random.randint(1, n_col) for i in range(n_peg)])
			population = remove_dups(population)

	return E_h


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
def play(n_col, n_peg, n_turns):
	
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
