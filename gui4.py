from tkinter import *                # python 3
from tkinter import font  as tkfont # python 3
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2
from combinatorics import all_colours
import random

class SampleApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Mastermind")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.combo = []
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

        button1 = Button(self, text="Select your color code",
                            command=lambda: controller.show_frame("ComboSelection"))
        button1.pack()


class ComboSelection(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="1. Select 4 colors for your combination", font=controller.title_font)
        label2 = Label(self, text="2. Click OK ", font=controller.title_font)
        label3 = Label(self, text="3. Start playing!", font=controller.title_font)
        
        label.pack(side="top", fill="x", pady=5)
        label2.pack(side="top", fill="x", pady=5)
        label3.pack(side="top", fill="x", pady=5)

        buttonRed = Button(self, text="Red", command=lambda: self.selectCombo("red"))
        buttonBlue = Button(self, text="Blue", command=lambda: self.selectCombo("blue"))
        buttonMagenta = Button(self, text="Magenta", command=lambda: self.selectCombo("magenta"))
        buttonGreen = Button(self, text="Green", command=lambda: self.selectCombo("green"))
        buttonPurple = Button(self, text="Purple", command=lambda: self.selectCombo("purple"))
        buttonYellow = Button(self, text="Yellow", command=lambda: self.selectCombo("yellow"))
        
        buttonOK = Button(self, text="OK", command=lambda: self.setCombo(controller))
        buttonPlay = Button(self, text="Let's play!", command=lambda: controller.show_frame("PlayGame"))

        buttonRed.pack()
        buttonBlue.pack()
        buttonMagenta.pack()
        buttonGreen.pack()
        buttonPurple.pack()
        buttonYellow.pack()
        buttonOK.pack(pady=10)
        buttonPlay.pack(pady=10)
        
        self.colorsSelected = 0
        self.combo = []

    def selectCombo(self, color):
      self.colorsSelected = self.colorsSelected + 1
      if self.colorsSelected <= 4:
          self.combo.append(color)
      else:
          pass
          # tkMessageBox.showwarning("Oops!", "Looks like you have already selected a combination!")


    def setCombo(self, controller):
        controller.combo = self.combo


class PlayGame(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.combo = []

        row_offset = 1
        number_of_positions = 4

        # print (("Your comboooo is '{}'").format(self.combo))
        showMyGuess = Button(self, text="Show my combo", command= lambda: self.show_my_combo(controller))
        showMyGuess.grid(row=row_offset, column=0)
        
        entryLabel = Label(self, text="Completely Correct:")
        entryLabel.grid(row=row_offset+1, sticky=E, padx=5, column=number_of_positions + 4)
        entryWidget_both = Entry(self)
        entryWidget_both["width"] = 5
        entryWidget_both.grid(row=row_offset+1, column=number_of_positions + 5)
        
        entryLabel = Label(self)
        entryLabel["text"] = "Wrong Position:"
        entryLabel.grid(row=row_offset+3, sticky=E, padx=5, column= number_of_positions + 4)
        entryWidget_only_colours = Entry(self)
        entryWidget_only_colours["width"] = 5
        entryWidget_only_colours.grid(row=row_offset+3, column=number_of_positions + 5)
        
        colors = ["red", "blue", "magenta", "green", "purple", "yellow"]
        init_guess = []

        while len(init_guess) < 4:
            i = random.randint(0, 5)
            if colors[i] not in init_guess:
                init_guess.append(colors[i])

        self.most_recent_guess = init_guess
        submit_button = Button(self, text="Submit")
        submit_button["command"] = lambda: self.eval_guess(entryWidget_both.get(), entryWidget_only_colours.get(), self.most_recent_guess)
        submit_button.grid(row=5,column=number_of_positions + 4)

        quit_button = Button(self, text="Quit", command=self.quit)
        quit_button.grid(row=5,column=number_of_positions + 5)

        self.show_current_guess(init_guess)
    

    def show_my_combo(self, controller):
        row = 2 
        Label(self, text="   Your combo is   ").grid(row=row, column=0, columnspan=4)
        row +=1
        col_count = 1
        for c in controller.combo:
            # print(c)
            l = Label(self, text="    ", bg=c)
            l.grid(row=row,column=col_count,  sticky=W, padx=2)
            col_count += 1


    def show_current_guess(self, new_guess):
        row = 4
        Label(self, text="   New Guess:   ").grid(row=row, column=0, columnspan=4)
        row +=1
        col_count = 1
        for c in new_guess:
            # print(c)
            l = Label(self, text="    ", bg=c)
            l.grid(row=row,column=col_count,  sticky=W, padx=2)
            col_count += 1


    def eval_guess(self, both, colors, most_recent_guess):
        if len(both) == 0:
            both = 0
        if len(colors) == 0:
            colors = 0
        eval_result = (both, colors)

        self.create_new_guess(eval_result, self.most_recent_guess) 
        

    ### eval_result is a tuple of (# color+position, #color only) of the most recent guess
    ### most_recent_guess is an array of the colors of the most recent guess
    def create_new_guess(self, eval_result, most_recent_guess):
        print ("the most recent guess is '{}'".format(most_recent_guess))
        
        ## in the end set the line below to the result (the green stuff is a placeholder)
        self.most_recent_guess = ["green", "green", "green", "green"]





    # def new_evaluation(self, current_colour_choices):
    #     rightly_positioned, permutated = get_evaluation()
    #     if rightly_positioned == number_of_positions:
    #         return(current_colour_choices, (rightly_positioned, permutated))
  
    #     if not reasonable(rightly_positioned, permutated):
    #         print("Input Error: Sorry, the input makes no sense")
    #         return(current_colour_choices, (-1, permutated))
    #     guesses.append((current_colour_choices, (rightly_positioned, permutated)))
    #     view_guesses()
  
    #     current_colour_choices = create_new_guess() 
    #     self.show_current_guess(current_colour_choices)
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









