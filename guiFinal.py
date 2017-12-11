from tkinter import *                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import messagebox
# from combinatorics import all_colours
import random
import numpy

class SampleApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Mastermind")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        container = Frame(self, width=200,height=100)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.combo = []
        self.num_pegs = 0
        self.num_cols = 0
        self.possible_cols = []
        self.frames = {}
        for F in (StartPage, ComboSelection, PlayGame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Welcome! Let's play Mastermind!", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        buttonNum_pegs_lbl = Label(self, text="Choose the number to have in your combination (must be between 4 and 6):")
        buttonNum_pegs = Entry(self)
        buttonNum_cols_lbl = Label(self, text="Choose the number of colors to select from (must be between 6 and 10):")
        buttonNum_cols = Entry(self)
        
        sub = Button(self, text="Submit", 
            command=lambda: self.set_nums(buttonNum_pegs.get(), buttonNum_cols.get(), controller))

        buttonNum_pegs_lbl.pack()
        buttonNum_pegs.pack()
        buttonNum_cols_lbl.pack()
        buttonNum_cols.pack()
        sub.pack()

    def set_nums(self, pegs, cols, controller):
        # print (int(pegs))
        if len(pegs) == 0:
            messagebox.showinfo("Default selection", "Default number for pegs: 4")
            pegs = 4
        if len(cols) == 0:
            messagebox.showinfo("Default selection", "Default number for colors: 6")
            cols = 6

        if int(pegs) < 4 or int(pegs) > 6:
            messagebox.showinfo("Invalid number of pegs", "Default number of pegs: 4")
            pegs = 4
        if int(cols) < 6 or int(cols) > 10:
            messagebox.showinfo("Invalid number of colors", "Default number of colors: 6")
            pegs = 6
        
        controller.num_pegs = int(pegs)
        controller.num_cols = int(cols)
        controller.show_frame("ComboSelection")

class ComboSelection(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        selectColors = Button(self, text="Select my combination", command=lambda: self.showButtons(controller))
        selectColors.pack()
        self.colorsSelected = 0
        self.combo = []

    def showButtons(self, controller):
        num_pegs = controller.num_pegs
        num_cols = controller.num_cols

        colors = ["navy", "gray", "maroon", "blue", "orange", "red", "magenta", "green", "purple", "yellow"]
        i = 0
        while i < controller.num_cols:
            button = Button(self, text=colors[i].title(), command=lambda i=i: self.selectCombo(colors[i], controller))
            button.pack()
            i = i+1

        controller.possible_cols = colors[0:controller.num_cols]
        buttonOK = Button(self, text="OK", command=lambda: self.setCombo(controller))
        buttonOK.pack(pady=10)

    def selectCombo(self, color, controller):
        self.colorsSelected = self.colorsSelected + 1
        if self.colorsSelected <= controller.num_pegs:
            self.combo.append(color)
        else:
            msg = "Looks like you have already selected a combination of " + str(controller.num_pegs) + " colors!"
            messagebox.showwarning("Oops!", msg)

    def setCombo(self, controller):
        controller.combo = self.combo
        controller.show_frame("PlayGame")


class PlayGame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.combo = []
        self.guesses = []
        self.responses = []
        self.letsGo = Button(self, text="Let's Play!", command= lambda: self.init_gui_game())
        self.letsGo.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.most_recent_guess = []
        self.grid_columnconfigure(1, minsize=50)  # Here
        
        self.P_CROSS_OVER = 0.5
        self.P_INVERT = 0.03
        self.P_MUTATE = 0.03
        self.P_PERMUTE = 0.03
        self.MAX_GEN = 150
        self.MAX_POP = 150
        self.REQ_FIT = 1


    def init_gui_game(self):
        self.show_my_combo()
        self.letsGo.destroy()

        row_offset = 1
        number_of_positions = self.controller.num_pegs
        
        entryLabel = Label(self, text="Completely Correct:")
        entryLabel.grid(row=row_offset+2, sticky=E, padx=5, column=number_of_positions + 7)
        entryWidget_both = Entry(self, width=5)
        entryWidget_both.grid(row=row_offset+2, column=number_of_positions + 8, padx=(0,20))
        
        entryLabel2 = Label(self, text= "Wrong Position:")
        entryLabel2.grid(row=row_offset+4, sticky=E, padx=5, column= number_of_positions + 7)
        entryWidget_only_colours = Entry(self, width=5)
        entryWidget_only_colours.grid(row=row_offset+4, column=number_of_positions + 8, padx=(0,20))            

        init_guess = []
        
        while len(init_guess) < self.controller.num_pegs:
            i = random.randint(1, self.controller.num_cols)
            if i not in init_guess:
                init_guess.append(i)

        self.most_recent_guess = init_guess
        self.guesses.append(init_guess)

        submit_button = Button(self, text="Submit")
        submit_button["command"] = lambda: self.eval_guess(entryWidget_both.get(), entryWidget_only_colours.get(), self.most_recent_guess)
        submit_button.grid(row=6,column=number_of_positions + 7)

        quit_button = Button(self, text="Quit", command=self.quit)
        quit_button.grid(row=6,column=number_of_positions + 8, padx=(0,20))

        self.show_current_guess(init_guess)


    def show_my_combo(self):
        row = 2 
        Label(self, text="   Your combo is   ").grid(row=row, column=0, columnspan=6)
        row +=1
        col_count = 2
        for c in self.controller.combo:
            # print(c)
            l = Label(self, text="    ", bg=c)
            l.grid(row=row,column=col_count,  sticky=W, padx=2)
            col_count += 1

    def idx_to_cols(self, guess):
        cols = []
        for i in guess:
            cols.append(self.controller.possible_cols[i-1])
        return cols

    def show_current_guess(self, new_guess):
        row = 4
        Label(self, text="   New Guess:   ").grid(row=row, column=0, columnspan=6)
        row +=1
        col_count = 2
        #print (("new guess is: '{}'").format(new_guess))
        guess = self.idx_to_cols(new_guess)
        #print (("new guess2 is: '{}'").format(guess))
        for c in guess:
            # print(c)
            l = Label(self, text="    ", bg=c)
            l.grid(row=row,column=col_count,  sticky=W, padx=2)
            col_count += 1
        self.view_old_guesses()

    def view_old_guesses(self):
        row = 6
        number_of_positions = self.controller.num_pegs
        Label(self, text="   Old Guesses:   ").grid(row=row, column=0, columnspan=6)
        Label(self, text="Color & Position").grid(row=row, padx=5, column=number_of_positions + 3)
        Label(self, text="Color Only").grid(row=row, padx=5, column=number_of_positions + 4)

        for idx in range(len(self.guesses)-2, -1, -1):
            # print (('{}').format(self.guesses[idx]))
            guess = self.idx_to_cols(self.guesses[idx])
            # print (('{}').format(guess))
            row += 1
            col_count = 2
            
            for c in guess:
                l = Label(self, text="    ", bg=c)
                l.grid(row=row,column=col_count, pady=2, sticky=W, padx=2)
                col_count += 1
            
            col_count += 1
            for i in self.responses[idx]:
                l = Label(self, text=i)
                l.grid(row=row,column=col_count, padx=2)  
                col_count += 1    

    def eval_guess(self, both, colors, most_recent_guess):
        if len(both) == 0:
            both = 0
        if len(colors) == 0:
            colors = 0
        eval_result = [int(both), int(colors)]
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
        #if random.random() < P_CROSS_OVER:
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
        g2 = this_option[:]
        for i in range(len(prev_guesses)):
            g1 = prev_guesses[i][:]

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

        # initialize the population and remove any duplicates
        population = [[random.randint(1, n_col) for i in range(n_peg)] for j in range(self.MAX_POP)]
        
        # h = iteration number
        h = 1
        # E = set of eligible/elite codes at iteration h
        E_h = []
        
        while(h <= self.MAX_GEN and len(E_h) <= self.MAX_POP):
            h += 1
            # first evaluate the population and take some of the best + some random
            fitness = []
            for indiv in population:
                fitness.append(self.get_fitness(prev_guesses, indiv, responses, n_peg))

            # the new generation will contain some of the best indivs in this gen + randoms,
            # crossed over offspring of some,
            # mutations of some
            # use fitness values as probabilities to choose best indivs to keep same
            new_gen = []
            for i in range(len(population)):
                if random.random() <= (2*n_peg - fitness[i])/sum(range(n_peg)):
                    new_gen.append(population[i])
                if len(new_gen) == int(self.MAX_POP*(1-self.P_CROSS_OVER)):
                    break
            
            # select parents from previous gen using fitness values as probabilities
            parents = []
            for i in range(len(population)):
                if random.random() <= (2*n_peg - fitness[i])/sum(range(n_peg)):
                    parents.append(population[i])
                if len(parents) == int(self.MAX_POP*self.P_CROSS_OVER-10):
                    break

            # add some random indiv to parental pool promote genetic diversity
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

            # add the kids to the new population
            new_gen.extend(children)

            #get fitness of the elements in this new gen
            fitness = []
            for indiv in new_gen:
                fitness.append((indiv,self.get_fitness(prev_guesses,indiv, responses, n_peg)))
            
            # eligible individuals have a fitness of 0
            for (indiv,f) in fitness:
                if f == 0:
                    E_h.append(indiv)

            # remove dups in eligibles
            E_h = self.remove_dups(E_h)

            population = E_h[:]
            # fill remaining spot with random and remove duplicates again
            while len(population) < self.MAX_POP:
                population.append([random.randint(1, n_col) for i in range(n_peg)])
                population = self.remove_dups(population)

        return E_h[0]


    def AI_play(self, responses, guesses):
        n_col = self.controller.num_cols
        n_peg = self.controller.num_pegs

        X_i = responses[-1][0]
        Y_i = responses[-1][1]
        if(X_i != n_peg):
            options = self.GA(n_peg, n_col, guesses, responses)
            curr_guess = options
            fitcg = self.get_fitness(self.guesses, curr_guess, self.responses, n_peg)
            print("fitness of choson: " + str(fitcg))

        # curr_guess = ["green", "green", "green", "green", "green", "green"]
        #print ("guess in here is '{}'".format(curr_guess))
        self.most_recent_guess = curr_guess
        self.guesses.append(curr_guess)
        self.show_current_guess(curr_guess)

        print(self.guesses)
        print(self.responses)





    # def new_evaluation(self, current_colour_choices, controller):
    #     rightly_positioned, permutated = get_evaluation()
    #     if rightly_positioned == number_of_positions:
    #         return(current_colour_choices, (rightly_positioned, permutated))
  
    #     if not reasonable(rightly_positioned, permutated):
    #         print("Input Error: Sorry, the input makes no sense")
    #         return(current_colour_choices, (-1, permutated))
    #     guesses.append((current_colour_choices, (rightly_positioned, permutated)))
    #     view_guesses()
  
    #     current_colour_choices = create_new_guess() 
    #     self.show_current_guess(current_colour_choices, controller)
    #     if not current_colour_choices:
    #         return(current_colour_choices, (-1, permutated))
    #     return(current_colour_choices, (rightly_positioned, permutated))


    # def inconsistent(p, guesses):
    #     for guess in guesses:
    #       res = check(guess[0], p)
    #       (rightly_positioned, permutated) = guess[1]
    #     if res != [rightly_positioned, permutated]:
    #      return True # inconsistent
    #     return False # i.e. consistent


    # def reasonable(right, color):
    #     return not ((right + color > 4) or (right + color < 2) or (right == 3 and color == 1))

    # def check(p1, p2):
    #     blacks = 0
    #     whites = 0
    #     for i in range(len(p1)):
    #         if p1[i] == p2[i]:
    #             blacks += 1
    #         else:
    #             if p1[i] in p2:
    #                 whites += 1
    #     return [blacks, whites] 


    # def create_new_guess():
    #     next_choice = next(permutation_iterator) 
    #     while inconsistent(next_choice, guesses):
    #       try:
    #          next_choice = next(permutation_iterator)
    #       except StopIteration:
    #          print("Error: Your answers were inconsistent!")
    #          return ()
    #     return next_choice


    # def new_evaluation_tk():
    #     global current_colour_choices
    #     res = new_evaluation(current_colour_choices)
    #     current_colour_choices = res[0]


    # def show_current_guess(self, new_guess):
    #     row = 1 
    #     Label(self, text="   New Guess:   ").grid(row=row, column=0, columnspan=4)
    #     row +=1
    #     col_count = 0
    #     for c in new_guess:
    #         print(c)
    #         l = Label(self, text="    ", bg=c)
    #         l.grid(row=row,column=col_count,  sticky=W, padx=2)
    #         col_count += 1


    # def view_guesses():
    #     row = 3
    #     Label(self, text="Old Guesses").grid(row=row, column=0, columnspan=4)
    #     Label(self, text="c&p").grid(row=row, padx=5, column=number_of_positions + 1)
    #     Label(self, text="p").grid(row=row, padx=5, column=number_of_positions + 2)
        
    #     # dummy label for distance:
    #     Label(self, text="         ").grid(row=row, column=number_of_positions + 3)


    #     row += 1
    #     # vertical dummy label for distance:
    #     Label(self, text="             ").grid(row=row, column=0, columnspan=5)

    #     for guess in guesses:
    #         guessed_colours = guess[0]
    #         col_count = 0
    #         row += 1
    #         for c in guessed_colours:
    #             print(guessed_colours[col_count])
    #             l = Label(self, text="    ", bg=guessed_colours[col_count])
    #             l.grid(row=row,column=col_count,  sticky=W, padx=2)
    #             col_count += 1
    #       # evaluation:
    #         for i in (0,1):
    #             l = Label(self, text=str(guess[1][i]))
    #             l.grid(row=row,column=col_count + i + 1, padx=2)



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()









