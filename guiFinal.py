from tkinter import *                # python 3
from tkinter import font  as tkfont  # python 3
from tkinter import messagebox
import random
import numpy

class Mastermind(Tk):

    # Initializes the controller for the game, which brings the appopriate frame forward
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Mastermind")
        self.title_font = tkfont.Font(family='MS Sans Serif', size=23, weight="bold")
        container = Frame(self, width=200,height=100)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.combo = []
        self.num_pegs = 0
        self.num_cols = 0
        self.possible_cols = []
        self.frames = {}

        # Initialize the different frames of the game
        for F in (StartPage, ComboSelection, PlayGame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            frame.pack_propagate(0)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    # Brings the frame requested forward for user to interact
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(Frame):

    # Initializes the frame where the user can pick 4-peg or 5-peg version
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, width=500, height=500, bg="SkyBlue1")
        self.controller = controller
        label = Label(self, text="Welcome! Let's play Mastermind!", bg="SkyBlue1", anchor=CENTER, font=controller.title_font)

        msg = Label(self, text="Select the version to play:", bg="SkyBlue1")
        v4 = Button(self, text="4-peg Combination", highlightbackground="SkyBlue1", command=lambda: self.set_nums(4))
        v5 = Button(self, text="5-peg Combination", highlightbackground="SkyBlue1", command=lambda: self.set_nums(5))
        dummy = Label(self, text= "           ", bg="SkyBlue1")
        
        dummy.pack()
        label.pack(side="top", fill="x", pady=10)
        msg.pack()
        v4.pack()
        v5.pack()

    # Sets the number of pegs and colors for the game. If the user selected 4 pegs, they can choose 
    # from 6 colors, if they selected 5 pegs, they can choose from 8 colors 
    def set_nums(self, pegs):
        if pegs == 4:
            cols = 6
        else:
            cols = 8
        self.controller.num_pegs = pegs
        self.controller.num_cols = cols
        self.controller.show_frame("ComboSelection")

class ComboSelection(Frame):

    # Initializes the frame in which the user can select a combination
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="SkyBlue1")
        self.controller = controller
       
        # Dummy labels for distance 
        dummy1 = Label(self, text = "    ", bg="SkyBlue1")
        dummy2 = Label(self, text = "    ", bg="SkyBlue1")
        dummy3 = Label(self, text = "    ", bg="SkyBlue1")
        selectColors = Button(self, text="Select my combination", highlightbackground="SkyBlue1", command=lambda: self.showButtons(controller))
        dummy1.pack()
        dummy2.pack()
        dummy3.pack()
        selectColors.pack()
        self.colorsSelected = 0
        self.combo = []

    def showButtons(self, controller):
        num_pegs = controller.num_pegs
        num_cols = controller.num_cols

        colors = ["navy", "gray", "maroon", "blue", "orange", "red", "magenta", "green", "purple", "yellow"]
        i = 0

        # Depending on the number of pegs, show 6 or 8 colors for user to choose from
        while i < controller.num_cols:
            button = Button(self, text=colors[i].title(), highlightbackground="SkyBlue1", command=lambda i=i: self.selectCombo(colors[i], controller))
            button.pack()
            i = i+1

        controller.possible_cols = colors[0:controller.num_cols]
        buttonOK = Button(self, text="OK", highlightbackground="SkyBlue1", command=lambda: self.setCombo(controller))
        buttonOK.pack(pady=10)

    # Adds a specific color to the combination of the user
    def selectCombo(self, color, controller):
        self.colorsSelected = self.colorsSelected + 1

        # If the user selects more than the specified number, show a pop-up message
        if self.colorsSelected <= controller.num_pegs:
            self.combo.append(color)
        else:
            msg = "Looks like you have already selected a combination of " + str(controller.num_pegs) + " colors!"
            messagebox.showwarning("Oops!", msg)

    # Sets the final combination
    def setCombo(self, controller):
        controller.combo = self.combo
        controller.show_frame("PlayGame")


class PlayGame(Frame):

    # Initializes the game-playing frame
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="SkyBlue1")
        self.controller = controller
        self.combo = []
        self.guesses = []
        self.responses = []
        self.letsGo = Button(self, text="Let's Play!", highlightbackground="SkyBlue1", command= lambda: self.init_gui_game())
        self.letsGo.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.most_recent_guess = []
        self.grid_columnconfigure(1, minsize=50)
        
        # Initialize parameters for Genetic Algorithm
        self.P_CROSS_OVER = 0.5
        self.P_MUTATE = 0.03
        self.MAX_GEN = 100
        self.MAX_POP = 150


    # GUI Implementation of game
    def init_gui_game(self):
        self.show_my_combo()
        self.letsGo.destroy()

        # Increase parameters for GA if 5-peg version is chosen
        if self.controller.num_pegs == 5:
        	self.MAX_GEN = 150
        	self.MAX_POP = 200

        row_offset = 1
        number_of_positions = self.controller.num_pegs
        
        entryLabel = Label(self, text="Completely Correct:", bg="SkyBlue1")
        entryLabel.grid(row=row_offset+2, sticky=E, padx=5, column=number_of_positions + 7)
        entryWidget_both = Entry(self, width=5, highlightbackground="SkyBlue1")
        entryWidget_both.grid(row=row_offset+2, column=number_of_positions + 8, padx=(0,20))
        
        entryLabel2 = Label(self, text= "Wrong Position:", bg="SkyBlue1")
        entryLabel2.grid(row=row_offset+4, sticky=E, padx=5, column= number_of_positions + 7)
        entryWidget_only_colours = Entry(self, width=5, highlightbackground="SkyBlue1")
        entryWidget_only_colours.grid(row=row_offset+4, column=number_of_positions + 8, padx=(0,20))            

        init_guess = []
        if self.controller.num_pegs == 4:
            init_guess = [1,2,1,4]
        else:
            # create a random initial guess
            while len(init_guess) < self.controller.num_pegs:
                i = random.randint(1, self.controller.num_cols)
                if i not in init_guess:
                    init_guess.append(i)
        
        self.most_recent_guess = init_guess

        # Add to the list of all guesses
        self.guesses.append(init_guess)

        submit_button = Button(self, text="Submit", highlightbackground="SkyBlue1")
        submit_button["command"] = lambda: self.eval_guess(entryWidget_both.get(), entryWidget_only_colours.get(), self.most_recent_guess)
        submit_button.grid(row=6,column=number_of_positions + 7)

        quit_button = Button(self, text="Quit", highlightbackground="SkyBlue1", command=self.quit)
        quit_button.grid(row=6,column=number_of_positions + 8, padx=(0,20))

        self.show_current_guess(init_guess)


    # GUI implementation for showing the combination of the user at the top of the frame
    def show_my_combo(self):
        row = 2 
        Label(self, text="   Your combo is   ", bg="SkyBlue1").grid(row=row, column=0, columnspan=6)
        row +=1
        col_count = 2
        for c in self.controller.combo:
            l = Label(self, text="    ", bg=c)
            l.grid(row=row,column=col_count,  sticky=W, padx=2)
            col_count += 1


    # Returns the actual colors from an array of indeces passed in guess. For example, [1,2,3,4]
    # would return ["navy", "gray", "maroon", "blue"]. Indeces in the arrays range from 1-6 (not 0-5)
    def idx_to_cols(self, guess):
        cols = []
        for i in guess:
            cols.append(self.controller.possible_cols[i-1])
        return cols


    # Shows most recent guess below the user's combination
    def show_current_guess(self, new_guess):
        row = 4
        Label(self, text="   New Guess:   ", bg="SkyBlue1").grid(row=row, column=0, columnspan=6)
        row +=1
        col_count = 2
        guess = self.idx_to_cols(new_guess)
        for c in guess:
            l = Label(self, text="    ", bg=c)
            l.grid(row=row,column=col_count,  sticky=W, padx=2)
            col_count += 1
        self.view_old_guesses()


    # Shows old guesses and responses underneath most recent guess, from newest to lowest
    def view_old_guesses(self):
        row = 6
        number_of_positions = self.controller.num_pegs
        Label(self, text="   Old Guesses:   ", bg="SkyBlue1").grid(row=row, column=0, columnspan=6)
        Label(self, text="Color & Position", bg="SkyBlue1").grid(row=row, padx=5, column=number_of_positions + 3)
        Label(self, text="Color Only", bg="SkyBlue1").grid(row=row, padx=5, column=number_of_positions + 4)

        for idx in range(len(self.guesses)-2, -1, -1):
            guess = self.idx_to_cols(self.guesses[idx])
            row += 1
            col_count = 2
            
            for c in guess:
                l = Label(self, text="    ", bg=c)
                l.grid(row=row,column=col_count, pady=2, sticky=W, padx=2)
                col_count += 1
            
            col_count += 1
            for i in self.responses[idx]:
                l = Label(self, text=i, bg="SkyBlue1")
                l.grid(row=row,column=col_count, padx=2)  
                col_count += 1    


    # Takes user reponses on the guess, and checks whether it is accurate
    # If not, shows pop-up message to prompt the user to re-enter the values
    def eval_guess(self, both, colors, most_recent_guess):
        # If user left a field blank, assume number of pegs is 0
        if len(both) == 0:
            both = 0
        if len(colors) == 0:
            colors = 0
        eval_result = [int(both), int(colors)]
        
        col_guess = self.idx_to_cols(most_recent_guess)
        right_num_cols = 0
        right_num_both = 0
        filter_guess = []
        filter_combo = []
        
        # Filter out all pegs that have both number of color and position correct
        for i in range(self.controller.num_pegs):
            if self.controller.combo[i] == col_guess[i]:
                right_num_both += 1
            else:
                filter_guess.append(col_guess[i])
                filter_combo.append(self.controller.combo[i])

        # Filter out pegs that have correct color
        for j in range(len(filter_combo)):
            if filter_guess[j] in filter_combo:
                right_num_cols += 1
                filter_combo.remove(filter_guess[j])

        if right_num_cols != eval_result[1] or right_num_both != eval_result[0]:
            messagebox.showinfo("Hey now!", "Check your responses!")
        else:
            if int(both) == self.controller.num_pegs:
                messagebox.showinfo("Game Over!", "Your combination was discovered.")
                self.quit()
            else:   
                self.responses.append(eval_result)
                self.AI_play(self.responses, self.guesses) 


#################################################################################
# GENETIC ALGORITHM FUNCTIONS
#################################################################################
        

    def remove_dups(self, mylist):
        seen = set()
        newlist = []
        for item in mylist:
            t = tuple(item)
            if t not in seen:
                newlist.append(item)
                seen.add(t)
        return newlist


    def cross_over(self, g1,g2, n_peg):
        # If random.random() < P_CROSS_OVER:
        cross_loc = random.randint(1, n_peg-1)
        new_g1 = g1[0:cross_loc] + g2[cross_loc:]
        new_g2 = g2[0:cross_loc] + g1[cross_loc:]
        return([new_g1, new_g2])


    def mutate(self, g1, n_peg, n_col):
        if(random.random() < self.P_MUTATE):
            loc = random.randint(0, n_peg-1)
            col = random.randint(1, n_col)
            g1[loc] = col
        return(g1)

    def get_fitness(self, prev_guesses, this_option, responses, n_peg):
        a = 1
        b = 2
        X_vals = []
        Y_vals = []
        for i in range(len(prev_guesses)):
            g1 = prev_guesses[i][:]
            g2 = this_option[:]

            X_i = responses[i][0]
            Y_i = responses[i][1]
            Xi_g2 = 0
            Yi_g2 = 0

            for i in range(len(g1)):
                if(g2[i] == g1[i]):
                    Xi_g2 += 1
                    g1[i] = 0
                    g2[i] = -1
            for i in range(len(g1)):
                if g2[i] in g1:
                    Yi_g2 += 1
                    idx = g1.index(g2[i])
                    g1[idx] = 0

            X_vals.append(abs(Xi_g2 - X_i))
            Y_vals.append(abs(Yi_g2 - Y_i))

        fitness_g2 = a * sum(X_vals) + sum(Y_vals) # + b * n_peg * (len(prev_guesses) -1)
        return(fitness_g2)


    def GA(self, n_peg, n_col, prev_guesses, responses):

        # Initialize the population and remove any duplicates
        population = [[random.randint(1, n_col) for i in range(n_peg)] for j in range(self.MAX_POP)]
        
        # h = iteration number
        h = 1
        # E = set of eligible/elite codes at iteration h
        E_h = []
        
        while(h <= self.MAX_GEN and len(E_h) <= self.MAX_POP):
            h += 1
            # First evaluate the population and take some of the best + some random
            fitness = []
            for indiv in population:
                fitness.append(self.get_fitness(prev_guesses, indiv, responses, n_peg))

            # The new generation will contain some of the best indivs in this gen + randoms,
            # crossed over offspring of some,
            # mutations of some
            # use fitness values as probabilities to choose best indivs to keep same
            new_gen = []
            for i in range(len(population)):
                if random.random() <= (2*n_peg - fitness[i])/sum(range(n_peg)):
                    new_gen.append(population[i])
                if len(new_gen) == int(self.MAX_POP*(1-self.P_CROSS_OVER)):
                    break
            
            # Select parents from previous gen using fitness values as probabilities
            parents = []
            for i in range(len(population)):
                if random.random() <= (2*n_peg - fitness[i])/sum(range(n_peg)):
                    parents.append(population[i])
                if len(parents) == int(self.MAX_POP*self.P_CROSS_OVER-10):
                    break

            # Add some random indiv to parental pool promote genetic diversity
            while len(parents) < int(self.MAX_POP*self.P_CROSS_OVER/2) * 2:
                parents.append([random.randint(1, n_col) for i in range(n_peg)])

            random.shuffle(parents)

            children = []
            i = 0
            while i < len(parents):
                child = self.cross_over(parents[i], parents[i+1], n_peg)
                if random.random() <= self.P_MUTATE:
                    child = [self.mutate(child[0],n_peg, n_col), self.mutate(child[1],n_peg, n_col)]
                children.extend(child)
                i += 2

            # Add the kids to the new population
            new_gen.extend(children)

            # Get fitness of the elements in this new gen
            fitness = []
            for indiv in new_gen:
                fitness.append((indiv,self.get_fitness(prev_guesses,indiv, responses, n_peg)))
            
            # Eligible individuals have a fitness of 0
            for (indiv,f) in fitness:
                if f == 0:
                    E_h.append(indiv)

            # Remove dups in eligibles
            E_h = self.remove_dups(E_h)

            population = E_h[:]
            # Fill remaining spot with random and remove duplicates again
            while len(population) < self.MAX_POP:
                population.append([random.randint(1, n_col) for i in range(n_peg)])
                population = self.remove_dups(population)

        return E_h[0]

    # Wrapper function for generation a new guess using GA
    def AI_play(self, responses, guesses):
        n_col = self.controller.num_cols
        n_peg = self.controller.num_pegs

        X_i = responses[-1][0]
        Y_i = responses[-1][1]
        if(X_i != n_peg):
            curr_guess = self.GA(n_peg, n_col, guesses, responses)

        self.most_recent_guess = curr_guess
        self.guesses.append(curr_guess)
        self.show_current_guess(curr_guess)


if __name__ == "__main__":
    game = Mastermind()
    game.mainloop()



# Helpful source for GUI: https://www.python-course.eu/tkinter_mastermind.php





