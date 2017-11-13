#!/usr/bin/env python

# source of algorithm: https://lirias.kuleuven.be/bitstream/123456789/164803/1/kbi_0806.pdf

import sys
import numpy
import tkinter
import random


def AI_play(code, n_col, n_peg, response):

	# if this is the first guess, generate randomly
	if response == NULL:
		# assign an interger to each possible color
		colors = range(1,n_col)
		# play initial random guess
		guess = numpy.random.choice(colors, n_pegs)

	else:
		X_i = response[0]
		Y_i = response[1]
		if(X_i != n_col):
			print("not perfect")
			# DO GENETIC ALG



def person_play(guess, code):
	# X_i = exact number of matches in iteration i (red pegs)
	X_i = 0
	# Y_i = number of partial matches in iteration i (white pegs)
	Y_i = 0

	# get info from GUI about response




# method that controls the alternating turns
def play(n_col, n_peg, n_turns,code):
	
	turn = 1
	response = NULL
	while(turn <= n_turns):

		if turn == 1:
			code = start_game()

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
